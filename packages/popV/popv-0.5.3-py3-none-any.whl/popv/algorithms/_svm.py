from __future__ import annotations

import logging
import os

import joblib
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.calibration import CalibratedClassifierCV

from popv import settings
from popv.algorithms._base_algorithm import BaseAlgorithm


class Support_Vector(BaseAlgorithm):
    """
    Class to compute LinearSVC.

    Parameters
    ----------
    batch_key
        Key in obs field of adata for batch information.
        Default is "_batch_annotation".
    labels_key
        Key in obs field of adata for cell-type information.
        Default is "_labels_annotation".
    layer_key
        Key in layers field of adata used for classification. By default uses 'X' (log1p10K).
    result_key
        Key in obs in which celltype annotation results are stored.
        Default is "popv_svm_prediction".
    classifier_dict
        Dictionary to supply non-default values for SVM classifier. Options at
        :class:`sklearn.svm.LinearSVC`.
        Default is {'C': 1, 'max_iter': 5000, 'class_weight': 'balanced'}.
    """

    def __init__(
        self,
        batch_key: str | None = "_batch_annotation",
        labels_key: str | None = "_labels_annotation",
        layer_key: str | None = None,
        result_key: str | None = "popv_svm_prediction",
        classifier_dict: str | None = {},
        train_both: bool = False,
    ) -> None:
        super().__init__(
            batch_key=batch_key,
            labels_key=labels_key,
            result_key=result_key,
        )

        self.layer_key = layer_key
        self.classifier_dict = {
            "C": 1,
            "max_iter": 5000,
            "class_weight": "balanced",
        }
        if classifier_dict is not None:
            self.classifier_dict.update(classifier_dict)
        self.train_both = train_both

    def predict(self, adata):
        """
        Predict celltypes using LinearSVC.

        Parameters
        ----------
        adata
            Anndata object. Results are stored in adata.obs[self.result_key].
        """
        logging.info(f'Computing support vector machine. Storing prediction in adata.obs["{self.result_key}"]')
        test_x = adata.layers[self.layer_key] if self.layer_key else adata.X

        if adata.uns["_prediction_mode"] == "retrain":
            train_idx = adata.obs["_ref_subsample"]
            train_x = adata[train_idx].layers[self.layer_key] if self.layer_key else adata[train_idx].X
            train_x = np.array(train_x.todense())
            train_y = adata.obs.loc[train_idx, self.labels_key].cat.codes.to_numpy()
            if settings.cuml:
                from cuml.svm import LinearSVC
                from sklearn.multiclass import OneVsRestClassifier

                self.classifier_dict["probability"] = self.return_probabilities
                clf = OneVsRestClassifier(LinearSVC(**self.classifier_dict))
                clf.fit(train_x, train_y)
                joblib.dump(
                    clf,
                    open(
                        os.path.join(
                            adata.uns["_save_path_trained_models"],
                            "svm_classifier_cuml.joblib",
                        ),
                        "wb",
                    ),
                )
                self.classifier_dict.pop("probability")
            if not settings.cuml or self.train_both:
                clf = CalibratedClassifierCV(svm.LinearSVC(**self.classifier_dict))
                clf.fit(train_x, train_y)
                joblib.dump(
                    clf,
                    open(
                        os.path.join(
                            adata.uns["_save_path_trained_models"],
                            "svm_classifier.joblib",
                        ),
                        "wb",
                    ),
                )

        if self.return_probabilities:
            required_columns = [self.result_key, f"{self.result_key}_probabilities"]
        else:
            required_columns = [self.result_key]

        result_df = pd.DataFrame(index=adata.obs_names, columns=required_columns, dtype=float)
        result_df[self.result_key] = result_df[self.result_key].astype("object")
        if settings.cuml:
            clf = joblib.load(
                open(
                    os.path.join(
                        adata.uns["_save_path_trained_models"],
                        "svm_classifier_cuml.joblib",
                    ),
                    "rb",
                )
            )
            shard_size = int(settings.shard_size)
            for i in range(0, adata.n_obs, shard_size):
                tmp_x = test_x[i : i + shard_size]
                names_x = adata.obs_names[i : i + shard_size]
                tmp_x = np.array(tmp_x.todense())
                result_df.loc[names_x, self.result_key] = adata.uns["label_categories"][clf.predict(tmp_x).astype(int)]
                if self.return_probabilities:
                    result_df.loc[names_x, f"{self.result_key}_probabilities"] = np.max(
                        clf.predict_proba(tmp_x), axis=1
                    ).astype(float)
        else:
            clf = joblib.load(
                open(
                    os.path.join(adata.uns["_save_path_trained_models"], "svm_classifier.joblib"),
                    "rb",
                )
            )
            result_df[self.result_key] = adata.uns["label_categories"][clf.predict(test_x)]
            if self.return_probabilities:
                result_df[f"{self.result_key}_probabilities"] = np.max(clf.predict_proba(test_x), axis=1)
        for col in required_columns:
            if col not in adata.obs.columns:
                adata.obs[col] = (
                    pd.Series(dtype="float64") if "probabilities" in col else adata.uns["unknown_celltype_label"]
                )
        adata.obs.loc[adata.obs["_predict_cells"] == "relabel", result_df.columns] = result_df
