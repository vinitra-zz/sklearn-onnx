# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import unittest
from distutils.version import StrictVersion
import onnx
import onnxruntime
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType, Int64TensorType
from skl2onnx.common.data_types import onnx_built_with_ml
from test_utils import (
    dump_data_and_model,
    fit_classification_model,
    fit_regression_model,
)


class TestSklearnAdaBoostModels(unittest.TestCase):
    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_classifier_samme_r(self):
        model, X_test = fit_classification_model(AdaBoostClassifier(
            n_estimators=10, algorithm="SAMME.R", random_state=42,
            base_estimator=DecisionTreeClassifier(
                max_depth=2, random_state=42)), 3)
        model_onnx = convert_sklearn(
            model,
            "AdaBoost classification",
            [("input", FloatTensorType((None, X_test.shape[1])))],
            target_opset=10
        )
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X_test,
            model,
            model_onnx,
            basename="SklearnAdaBoostClassifierSAMMER",
            allow_failure="StrictVersion("
            "onnxruntime.__version__)"
            "<= StrictVersion('0.2.1')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_classifier_samme_r_logreg(self):
        model, X_test = fit_classification_model(AdaBoostClassifier(
            n_estimators=5, algorithm="SAMME.R",
            base_estimator=LogisticRegression(
                solver='liblinear')), 4)
        model_onnx = convert_sklearn(
            model,
            "AdaBoost classification",
            [("input", FloatTensorType((None, X_test.shape[1])))],
            target_opset=10
        )
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X_test,
            model,
            model_onnx,
            basename="SklearnAdaBoostClassifierSAMMERLogReg",
            allow_failure="StrictVersion("
            "onnxruntime.__version__)"
            "<= StrictVersion('0.2.1')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_classifier_samme(self):
        model, X_test = fit_classification_model(AdaBoostClassifier(
            n_estimators=5, algorithm="SAMME", random_state=42,
            base_estimator=DecisionTreeClassifier(
                max_depth=6, random_state=42)), 2)
        model_onnx = convert_sklearn(
            model,
            "AdaBoostClSamme",
            [("input", FloatTensorType((None, X_test.shape[1])))],
            target_opset=10,
        )
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X_test,
            model,
            model_onnx,
            basename="SklearnAdaBoostClassifierSAMMEDT",
            allow_failure="StrictVersion("
            "onnxruntime.__version__)"
            "< StrictVersion('0.5.0')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_classifier_lr(self):
        model, X_test = fit_classification_model(
            AdaBoostClassifier(learning_rate=0.3, random_state=42), 3,
            is_int=True)
        model_onnx = convert_sklearn(
            model,
            "AdaBoost classification",
            [("input", Int64TensorType((None, X_test.shape[1])))],
            target_opset=10
        )
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X_test,
            model,
            model_onnx,
            basename="SklearnAdaBoostClassifierLR",
            allow_failure="StrictVersion("
            "onnxruntime.__version__)"
            "<= StrictVersion('0.2.1')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_regressor(self):
        model, X = fit_regression_model(
            AdaBoostRegressor(n_estimators=5))
        model_onnx = convert_sklearn(
            model, "AdaBoost regression",
            [("input", FloatTensorType([None, X.shape[1]]))],
            target_opset=10)
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X,
            model,
            model_onnx,
            basename="SklearnAdaBoostRegressor-Dec4",
            allow_failure="StrictVersion("
            "onnxruntime.__version__) "
            "< StrictVersion('0.5.0') or "
            "StrictVersion(onnx.__version__) "
            "== StrictVersion('1.4.1')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_regressor_lreg(self):
        model, X = fit_regression_model(
            AdaBoostRegressor(n_estimators=5,
                              base_estimator=LinearRegression()))
        model_onnx = convert_sklearn(
            model, "AdaBoost regression",
            [("input", FloatTensorType([None, X.shape[1]]))],
            target_opset=10)
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X,
            model,
            model_onnx,
            basename="SklearnAdaBoostRegressorLReg-Dec4",
            allow_failure="StrictVersion("
            "onnxruntime.__version__) "
            "< StrictVersion('0.5.0') or "
            "StrictVersion(onnx.__version__) "
            "== StrictVersion('1.4.1')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_regressor_int(self):
        model, X = fit_regression_model(
            AdaBoostRegressor(n_estimators=5), is_int=True)
        model_onnx = convert_sklearn(
            model, "AdaBoost regression",
            [("input", Int64TensorType([None, X.shape[1]]))],
            target_opset=10)
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X,
            model,
            model_onnx,
            basename="SklearnAdaBoostRegressorInt",
            allow_failure="StrictVersion("
            "onnxruntime.__version__) "
            "< StrictVersion('0.5.0') or "
            "StrictVersion(onnx.__version__) "
            "== StrictVersion('1.4.1')",
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_regressor_lr10(self):
        model, X = fit_regression_model(
            AdaBoostRegressor(learning_rate=0.5, random_state=42))
        model_onnx = convert_sklearn(
            model, "AdaBoost regression",
            [("input", FloatTensorType([None, X.shape[1]]))],
            target_opset=10)
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X,
            model,
            model_onnx,
            basename="SklearnAdaBoostRegressorLR-Dec4",
            allow_failure="StrictVersion("
            "onnxruntime.__version__) "
            "< StrictVersion('0.5.0') or "
            "StrictVersion(onnx.__version__) "
            "== StrictVersion('1.4.1')",
            verbose=False
        )

    @unittest.skipIf(not onnx_built_with_ml(),
                     reason="Requires ONNX-ML extension.")
    @unittest.skipIf((StrictVersion(onnxruntime.__version__) <
                      StrictVersion("0.5.9999")),
                     reason="not available")
    @unittest.skipIf((StrictVersion(onnx.__version__) <
                      StrictVersion("1.5.0")),
                     reason="not available")
    def test_ada_boost_regressor_lr11(self):
        model, X = fit_regression_model(
            AdaBoostRegressor(learning_rate=0.5, random_state=42))
        model_onnx = convert_sklearn(
            model, "AdaBoost regression",
            [("input", FloatTensorType([None, X.shape[1]]))],
            target_opset=11)
        self.assertIsNotNone(model_onnx)
        dump_data_and_model(
            X,
            model,
            model_onnx,
            basename="SklearnAdaBoostRegressorLR-Dec4",
            allow_failure="StrictVersion("
            "onnxruntime.__version__) "
            "< StrictVersion('0.5.9999') or "
            "StrictVersion(onnx.__version__) "
            "== StrictVersion('1.4.1')",
            verbose=False
        )


if __name__ == "__main__":
    unittest.main()
