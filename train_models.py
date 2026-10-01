import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from src.features.engineering import compute_domain_features, ALL_FEATURE_COLUMNS
from src.evaluation.metrics import evaluate_classification

def train_and_export_models():
    os.makedirs("models/detection", exist_ok=True)
    os.makedirs("models/classification", exist_ok=True)
    os.makedirs("reports/results", exist_ok=True)
    
    # 1. Load Processed Data
    df_raw = pd.read_csv("data/raw/Marine_Engine_Fault_Data/marine_engine_telemetry.csv")
    df_features = compute_domain_features(df_raw)
    
    X = df_features[ALL_FEATURE_COLUMNS]
    y_detect = df_features["is_fault"]
    y_class = df_features["fault_class"]
    
    # Split
    X_tr_d, X_te_d, y_tr_d, y_te_d = train_test_split(X, y_detect, test_size=0.2, random_state=42, stratify=y_detect)
    X_tr_c, X_te_c, y_tr_c, y_te_c = train_test_split(X, y_class, test_size=0.2, random_state=42, stratify=y_class)
    
    print("--- 1. Training Binary Anomaly Detection Models ---")
    # Detection Model: LightGBM
    det_model = LGBMClassifier(n_estimators=150, max_depth=6, learning_rate=0.05, random_state=42, verbose=-1)
    det_model.fit(X_tr_d, y_tr_d)
    
    y_pred_d = det_model.predict(X_te_d)
    y_prob_d = det_model.predict_proba(X_te_d)
    det_metrics = evaluate_classification(y_te_d, y_pred_d, y_prob_d)
    print(f"Detection Model Accuracy: {det_metrics['accuracy'] * 100:.2f}%, F1: {det_metrics['f1_score']:.4f}")
    
    # Save detection model & feature column names
    joblib.dump({
        "model": det_model,
        "features": ALL_FEATURE_COLUMNS,
        "metrics": det_metrics
    }, "models/detection/marine_fault_detector.joblib")
    
    print("\n--- 2. Training Multi-Class Fault Diagnosis Models ---")
    # Classification Model: XGBoost
    cls_model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.08,
        objective="multi:softprob",
        random_state=42,
        eval_metric="mlogloss"
    )
    cls_model.fit(X_tr_c, y_tr_c)
    
    y_pred_c = cls_model.predict(X_te_c)
    y_prob_c = cls_model.predict_proba(X_te_c)
    cls_metrics = evaluate_classification(y_te_c, y_pred_c, y_prob_c)
    print(f"Fault Classification Accuracy: {cls_metrics['accuracy'] * 100:.2f}%, F1: {cls_metrics['f1_score']:.4f}")
    
    # Save classification model & metadata
    joblib.dump({
        "model": cls_model,
        "features": ALL_FEATURE_COLUMNS,
        "metrics": cls_metrics,
        "classes": {
            0: "Normal Operation",
            1: "Turbocharger / Turbine Fouling",
            2: "Fuel Injector Malfunction",
            3: "Scavenge Fire / High Thermal Load",
            4: "Cooling System Degradation",
            5: "Lube Oil & Bearing Wear"
        }
    }, "models/classification/marine_fault_classifier.joblib")
    
    print("\n[SUCCESS] Models trained and exported successfully!")

if __name__ == "__main__":
    train_and_export_models()
