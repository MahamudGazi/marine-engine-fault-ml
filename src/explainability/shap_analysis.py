import numpy as np
import pandas as pd
import shap

class MarineEngineExplainer:
    """
    Explainability engine using SHAP TreeExplainer for rapid inference-time attribution.
    """
    def __init__(self, model, feature_names=None):
        self.model = model
        self.feature_names = feature_names
        self.explainer = shap.TreeExplainer(model)

    def explain_sample(self, feature_df: pd.DataFrame, top_k=5, class_idx=None):
        """
        Computes SHAP values for a single input telemetry sample and returns top_k positive and negative drivers.
        """
        shap_values = self.explainer.shap_values(feature_df)
        
        # Handle binary vs multi-class shap output structures
        if isinstance(shap_values, list):
            # List of arrays per class (e.g. multi-class)
            if class_idx is not None and class_idx < len(shap_values):
                sample_shap = shap_values[class_idx][0]
            else:
                sample_shap = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
        elif isinstance(shap_values, np.ndarray):
            if shap_values.ndim == 3: # (samples, features, classes)
                idx = class_idx if (class_idx is not None and class_idx < shap_values.shape[2]) else 1
                sample_shap = shap_values[0, :, idx]
            elif shap_values.ndim == 2:
                sample_shap = shap_values[0]
            else:
                sample_shap = shap_values
        else:
            sample_shap = np.zeros(feature_df.shape[1])

        features = self.feature_names if self.feature_names is not None else feature_df.columns.tolist()
        values = feature_df.iloc[0].values

        attributions = []
        for feat, val, sv in zip(features, values, sample_shap):
            attributions.append({
                "feature": feat,
                "value": float(val),
                "shap_value": float(sv),
                "impact": "increases_fault_risk" if sv > 0 else "decreases_fault_risk"
            })

        # Sort by absolute SHAP impact
        attributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        return attributions[:top_k]
