from __future__ import annotations

import logging
import os

import joblib
import numpy as np
import scanpy as sc
from scipy.stats import mode
from sklearn.neighbors import KNeighborsClassifier

from popv import settings
from popv.algorithms._base_algorithm import BaseAlgorithm


class KNN_BBKNN(BaseAlgorithm):
    """
    Class to compute KNN classifier after BBKNN integration.

    Parameters
    ----------
    batch_key
        Key in obs field of adata for batch information. Default is "_batch_annotation".
    labels_key
        Key in obs field of adata for cell-type information. Default is "_labels_annotation".
    result_key
        Key in obs in which celltype annotation results are stored.
        Default is "popv_knn_bbknn_prediction".
    umap_key
        Key in obsm in which UMAP embedding of integrated data is stored.
        Default is "X_umap_bbknn_popv".
    method_kwargs
        Additional parameters for BBKNN.
        See :func:`scanpy.external.pp.bbknn`.
        Default is {"metric": "euclidean", "approx": True, "n_pcs": 50, "neighbors_within_batch": 3, "use_annoy": False}.
    classifier_kwargs
        Dictionary to supply non-default values for KNN classifier.
        See :class:`sklearn.neighbors.KNeighborsClassifier`.
        Default is {"weights": "uniform", "n_neighbors": 15}.
    embedding_kwargs
        Dictionary to supply non-default values for UMAP embedding.
        See :func:`scanpy.tl.umap`.
        Default is {"min_dist": 0.1}.
    """

    def __init__(
        self,
        batch_key: str | None = "_batch_annotation",
        labels_key: str | None = "_labels_annotation",
        result_key: str | None = "popv_knn_bbknn_prediction",
        umap_key: str | None = "X_umap_bbknn_popv",
        method_kwargs: dict | None = None,
        classifier_kwargs: dict | None = None,
        embedding_kwargs: dict | None = None,
    ) -> None:
        super().__init__(
            batch_key=batch_key,
            labels_key=labels_key,
            result_key=result_key,
            umap_key=umap_key,
        )
        if embedding_kwargs is None:
            embedding_kwargs = {}
        if classifier_kwargs is None:
            classifier_kwargs = {}
        if method_kwargs is None:
            method_kwargs = {}

        self.method_kwargs = {
            "metric": "euclidean",
            "approx": True,
            "n_pcs": 50,
            "neighbors_within_batch": 3,
            "use_annoy": False,
        }
        self.method_kwargs.update(method_kwargs)

        self.classifier_kwargs = {"weights": "uniform", "n_neighbors": 15}
        if classifier_kwargs is not None:
            self.classifier_kwargs.update(classifier_kwargs)

        self.embedding_kwargs = {"min_dist": 0.1}
        self.embedding_kwargs.update(embedding_kwargs)

    def compute_integration(self, adata):
        """
        Compute BBKNN integration.

        Parameters
        ----------
        adata
            AnnData object. Modified inplace.
        """
        logging.info("Integrating data with bbknn")
        if (
            adata.uns["_prediction_mode"] == "inference"
            and "X_umap_bbknn" in adata.obsm
            and not settings.recompute_embeddings
        ):
            index = joblib.load(os.path.join(adata.uns["_save_path_trained_models"], "pynndescent_index.joblib"))
            query_features = adata.obsm["X_pca"][adata.obs["_dataset"] == "query", :]
            indices, _ = index.query(query_features.astype(np.float32), k=5)

            neighbor_embedding = adata.obsm["X_umap_bbknn"][adata.obs["_dataset"] == "ref", :][indices].astype(
                np.float32
            )
            adata.obsm[self.umap_key][adata.obs["_dataset"] == "query", :] = np.mean(neighbor_embedding, axis=1)
            adata.obsm[self.umap_key] = adata.obsm[self.umap_key].astype(np.float32)

            neighbor_probabilities = adata.obs[f"{self.result_key}_probabilities"][adata.obs["_dataset"] == "ref", :][
                indices
            ].astype(np.float32)
            adata.obs.loc[adata.obs["_dataset"] == "query", f"{self.result_key}_probabilities"] = np.mean(
                neighbor_probabilities, axis=1
            )

            neighbor_prediction = adata.obs[f"{self.result_key}"][adata.obs["_dataset"] == "ref", :][indices].astype(
                np.float32
            )
            adata.obs.loc[adata.obs["_dataset"] == "query", f"{self.result_key}"] = mode(neighbor_prediction, axis=1)
        else:
            if len(adata.obs[self.batch_key].unique()) > 100:
                logging.warning("Using PyNNDescent instead of FAISS as high number of batches leads to OOM.")
                self.method_kwargs["neighbors_within_batch"] = 1  # Reduce memory usage.
                self.method_kwargs["pynndescent_n_neighbors"] = 10  # Reduce memory usage.
                sc.external.pp.bbknn(
                    adata, batch_key=self.batch_key, use_faiss=False, use_rep="X_pca", **self.method_kwargs
                )
            else:
                sc.external.pp.bbknn(
                    adata, batch_key=self.batch_key, use_faiss=True, use_rep="X_pca", **self.method_kwargs
                )

    def predict(self, adata):
        """
        Predict celltypes using Celltypist.

        Parameters
        ----------
        adata
            Anndata object. Results are stored in adata.obs[self.result_key].
        """
        logging.info(f'Saving knn on bbknn results to adata.obs["{self.result_key}"]')

        distances = adata.obsp["distances"]
        ref_idx = adata.obs["_labelled_train_indices"]
        ref_dist_idx = np.where(ref_idx)[0]
        train_y = adata.obs.loc[ref_idx, self.labels_key].cat.codes.to_numpy()
        train_distances = distances[ref_dist_idx, :][:, ref_dist_idx]
        test_distances = distances[:, :][:, ref_dist_idx]

        # Make sure BBKNN found the required number of neighbors, otherwise reduce n_neighbors for KNN.
        smallest_neighbor_graph = np.min(
            [
                np.diff(test_distances.indptr).min(),
                np.diff(train_distances.indptr).min(),
            ]
        )
        if smallest_neighbor_graph < self.classifier_kwargs["n_neighbors"]:
            logging.warning(f"BBKNN found only {smallest_neighbor_graph} neighbors. Reduced neighbors in KNN.")
            self.classifier_kwargs["n_neighbors"] = smallest_neighbor_graph

        knn = KNeighborsClassifier(metric="precomputed", **self.classifier_kwargs)
        knn.fit(train_distances, y=train_y)
        adata.obs[self.result_key] = adata.uns["label_categories"][knn.predict(test_distances)]

        if self.return_probabilities:
            adata.obs[f"{self.result_key}_probabilities"] = np.max(knn.predict_proba(test_distances), axis=1)

    def compute_umap(self, adata):
        """
        Compute UMAP embedding of integrated data.

        Parameters
        ----------
        adata
            AnnData object. Results are stored in adata.obsm[self.umap_key].
        """
        if self.compute_umap_embedding:
            logging.info(f'Saving UMAP of bbknn results to adata.obs["{self.embedding_key}"]')
            if len(adata.obs[self.batch_key]) < 30 and settings.cuml:
                method = "rapids"
            else:
                logging.warning("Using UMAP instead of RAPIDS as high number of batches leads to OOM.")
                method = "umap"
                # RAPIDS not possible here as number of batches drastically increases GPU RAM.
            adata.obsm[self.umap_key] = sc.tl.umap(adata, copy=True, method=method, **self.embedding_kwargs).obsm[
                "X_umap"
            ]
