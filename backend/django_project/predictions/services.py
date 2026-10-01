import os
import joblib
import pandas as pd
import numpy as np
import shap
from pathlib import Path

# Paths
def get_model_path(model_rel_path):
    possible_roots = [
        Path(__file__).resolve().parent.parent.parent.parent, # workspace root
        Path(__file__).resolve().parent.parent.parent,        # backend root
        Path(__file__).resolve().parent.parent,               # django_project root
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent
    ]
    for r in possible_roots:
        candidate = r / model_rel_path
        if candidate.exists():
            return candidate
    return possible_roots[0] / model_rel_path

DETECTION_MODEL_PATH = get_model_path(Path("models") / "detection" / "marine_fault_detector.joblib")
CLASSIFICATION_MODEL_PATH = get_model_path(Path("models") / "classification" / "marine_fault_classifier.joblib")

class MarineInferenceService:
    _instance = None
    
    def __init__(self):
        self.detector_data = None
        self.classifier_data = None
        self.detector_model = None
        self.classifier_model = None
        self.feature_columns = None
        self.classes = {}
        self.shap_explainer = None
        self.load_models()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_models(self):
        if DETECTION_MODEL_PATH.exists():
            self.detector_data = joblib.load(DETECTION_MODEL_PATH)
            self.detector_model = self.detector_data["model"]
            self.feature_columns = self.detector_data["features"]
            
        if CLASSIFICATION_MODEL_PATH.exists():
            self.classifier_data = joblib.load(CLASSIFICATION_MODEL_PATH)
            self.classifier_model = self.classifier_data["model"]
            self.classes = self.classifier_data.get("classes", {
                0: "Normal Operation",
                1: "Turbocharger / Turbine Fouling",
                2: "Fuel Injector Malfunction",
                3: "Scavenge Fire / High Thermal Load",
                4: "Cooling System Degradation",
                5: "Lube Oil & Bearing Wear"
            })
            # Setup SHAP Explainer on classifier
            try:
                self.shap_explainer = shap.TreeExplainer(self.classifier_model)
            except Exception as e:
                print(f"SHAP initialization warning: {e}")

    def compute_features(self, raw_dict: dict) -> pd.DataFrame:
        df = pd.DataFrame([raw_dict])
        
        cyl_cols = [
            "exhaust_temp_cyl1_c", "exhaust_temp_cyl2_c", "exhaust_temp_cyl3_c",
            "exhaust_temp_cyl4_c", "exhaust_temp_cyl5_c", "exhaust_temp_cyl6_c"
        ]
        
        # 1. Thermal Balance
        df["cyl_temp_mean"] = df[cyl_cols].mean(axis=1)
        df["cyl_temp_std"] = df[cyl_cols].std(axis=1)
        df["cyl_temp_max_spread"] = df[cyl_cols].max(axis=1) - df[cyl_cols].min(axis=1)
        
        # 2. Turbine Thermal Gradient
        df["turbine_delta_temp"] = df["exhaust_temp_inlet_c"] - df["exhaust_temp_outlet_c"]
        df["turbine_temp_ratio"] = df["exhaust_temp_inlet_c"] / (df["exhaust_temp_outlet_c"] + 1e-5)
        
        # 3. Turbocharger Compression Ratio Proxy
        df["turbo_pressure_ratio"] = df["scavenge_air_press_bar"] / 1.013
        df["turbo_speed_to_scavenge"] = df["turbocharger_rpm"] / (df["scavenge_air_press_bar"] + 1e-5)
        
        # 4. Coolant Delta T
        df["coolant_delta_t"] = df["coolant_outlet_temp_c"] - df["coolant_inlet_temp_c"]
        
        # 5. Lube Oil Delta T
        df["lube_oil_delta_t"] = df["lube_oil_outlet_temp_c"] - df["lube_oil_inlet_temp_c"]
        
        # 6. Specific Fuel Ratio
        df["fuel_to_load_ratio"] = df["fuel_flow_rate_kgh"] / (df["engine_load_pct"] + 1e-5)
        
        # Return properly ordered features
        return df[self.feature_columns]

    def predict(self, raw_telemetry: dict):
        if not self.classifier_model:
            self.load_models()
            
        features_df = self.compute_features(raw_telemetry)
        
        # 1. Anomaly Detection
        is_anomaly = bool(self.detector_model.predict(features_df)[0] == 1) if self.detector_model else False
        anomaly_prob = float(self.detector_model.predict_proba(features_df)[0][1]) if self.detector_model else 0.0
        
        # 2. Multi-class Fault Classification
        probs = self.classifier_model.predict_proba(features_df)[0]
        pred_class_idx = int(np.argmax(probs))
        confidence = float(probs[pred_class_idx]) * 100.0
        fault_name = self.classes.get(pred_class_idx, "Unknown Fault")
        
        prob_dict = {self.classes.get(i, f"Class {i}"): round(float(p) * 100, 2) for i, p in enumerate(probs)}
        
        # 3. SHAP Feature Attribution
        shap_explanations = []
        if self.shap_explainer is not None:
            try:
                raw_shap = self.shap_explainer.shap_values(features_df)
                if isinstance(raw_shap, list):
                    sample_shap = raw_shap[pred_class_idx][0]
                elif isinstance(raw_shap, np.ndarray) and raw_shap.ndim == 3:
                    sample_shap = raw_shap[0, :, pred_class_idx]
                elif isinstance(raw_shap, np.ndarray) and raw_shap.ndim == 2:
                    sample_shap = raw_shap[0]
                else:
                    sample_shap = np.zeros(len(self.feature_columns))
                    
                vals = features_df.iloc[0].values
                for feat, val, sv in zip(self.feature_columns, vals, sample_shap):
                    shap_explanations.append({
                        "feature": feat,
                        "value": round(float(val), 2),
                        "shap_value": round(float(sv), 4),
                        "impact": "Increases Risk" if sv > 0 else "Normalizing"
                    })
                shap_explanations.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
                shap_explanations = shap_explanations[:8]
            except Exception as e:
                print(f"SHAP explanation computation error: {e}")

        return {
            "is_anomaly": is_anomaly,
            "anomaly_probability": round(anomaly_prob * 100, 2),
            "fault_code": pred_class_idx,
            "fault_name": fault_name,
            "confidence_pct": round(confidence, 2),
            "class_probabilities": prob_dict,
            "shap_explanations": shap_explanations
        }

# Global singleton
ml_service = MarineInferenceService.get_instance()
