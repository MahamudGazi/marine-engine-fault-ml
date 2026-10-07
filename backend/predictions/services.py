import joblib
import numpy as np
import pandas as pd
import shap
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DETECTION_MODEL_PATH = PROJECT_ROOT / "models" / "detection" / "marine_fault_detector.joblib"
CLASSIFICATION_MODEL_PATH = PROJECT_ROOT / "models" / "classification" / "marine_fault_classifier.joblib"


class MarineInferenceService:
    _instance = None

    def __init__(self):
        self.detector_data = None
        self.classifier_data = None
        self.detector_model = None
        self.classifier_model = None
        self.feature_columns = []
        self.classes = {}
        self.simulation_profiles = {}
        self.shap_explainer = None
        self.load_models()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_models(self):
        if not DETECTION_MODEL_PATH.exists() or not CLASSIFICATION_MODEL_PATH.exists():
            raise FileNotFoundError(
                "Trained fault models are missing. Run `python train_models.py` from the project root."
            )
        self.detector_data = joblib.load(DETECTION_MODEL_PATH)
        self.classifier_data = joblib.load(CLASSIFICATION_MODEL_PATH)
        self.detector_model = self.detector_data["model"]
        self.classifier_model = self.classifier_data["model"]
        self.feature_columns = self.classifier_data["features"]
        if self.detector_data["features"] != self.feature_columns:
            raise ValueError("Detection and classification models use different feature schemas.")
        self.classes = self.classifier_data["classes"]
        self.simulation_profiles = {
            **self.detector_data.get("simulation_profiles", {}),
            **self.classifier_data.get("simulation_profiles", {}),
        }
        try:
            self.shap_explainer = shap.TreeExplainer(self.classifier_model)
        except Exception as exc:
            print(f"SHAP initialization warning: {exc}")

    def prepare_features(self, telemetry: dict) -> pd.DataFrame:
        missing = [name for name in self.feature_columns if name not in telemetry]
        if missing:
            raise ValueError(f"Missing required telemetry fields: {', '.join(missing)}")
        values = {name: telemetry[name] for name in self.feature_columns}
        frame = pd.DataFrame([values], columns=self.feature_columns)
        frame = frame.replace([np.inf, -np.inf], np.nan)
        medians = self.classifier_data.get("imputation_values", {})
        return frame.fillna(pd.Series(medians)).fillna(0.0)

    def predict(self, raw_telemetry: dict):
        features = self.prepare_features(raw_telemetry)
        detector_classes = list(self.detector_model.classes_)
        anomaly_col = detector_classes.index(1)
        anomaly_probability = float(self.detector_model.predict_proba(features)[0][anomaly_col])
        is_anomaly = bool(self.detector_model.predict(features)[0] == 1)

        probabilities = self.classifier_model.predict_proba(features)[0]
        class_codes = [int(code) for code in self.classifier_model.classes_]
        best_position = int(np.argmax(probabilities))
        predicted_code = class_codes[best_position]
        fault_name = self.classes[predicted_code] if is_anomaly else "Normal Operation"
        confidence = float(probabilities[best_position] * 100) if is_anomaly else (1 - anomaly_probability) * 100
        probability_map = {
            self.classes[code]: round(float(prob), 2)
            for code, prob in zip(class_codes, probabilities * 100)
        }

        explanations = []
        if is_anomaly and self.shap_explainer is not None:
            try:
                values = self.shap_explainer.shap_values(features)
                if isinstance(values, list):
                    contribution = np.asarray(values[best_position])[0]
                else:
                    values = np.asarray(values)
                    contribution = values[0, :, best_position] if values.ndim == 3 else values[0]
                for feature, value, shap_value in zip(self.feature_columns, features.iloc[0], contribution):
                    explanations.append({
                        "feature": feature,
                        "value": round(float(value), 4),
                        "shap_value": round(float(shap_value), 6),
                        "impact": "Increases Risk" if shap_value > 0 else "Normalizing",
                    })
                explanations.sort(key=lambda item: abs(item["shap_value"]), reverse=True)
                explanations = explanations[:8]
            except Exception as exc:
                print(f"SHAP explanation computation error: {exc}")

        return {
            "is_anomaly": is_anomaly,
            "anomaly_probability": round(anomaly_probability * 100, 2),
            "fault_code": predicted_code if is_anomaly else 0,
            "fault_name": fault_name,
            "confidence_pct": round(confidence, 2),
            "class_probabilities": probability_map,
            "shap_explanations": explanations,
        }


ml_service = MarineInferenceService.get_instance()
