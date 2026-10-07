"""Train experiment-aware models from the processed real marine dataset."""

from __future__ import annotations

import json
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GroupShuffleSplit

from src.data.loader import FAULT_CLASS_MAP, FAULT_DISPLAY_NAMES
from src.evaluation.metrics import evaluate_classification


ROOT = Path(__file__).resolve().parent
DETECTION_DATA = ROOT / "data" / "processed" / "detection_dataset.parquet"
CLASSIFICATION_DATA = ROOT / "data" / "processed" / "classification_dataset.parquet"
MODEL_DIR = ROOT / "models"
RESULT_DIR = ROOT / "reports" / "results"

TARGET_COLUMNS = {"Anomaly State", "anomaly_target", "target_name", "fault_class", "fault_name"}
METADATA_COLUMNS = {"source_file", "dataset_type", "fault_type"}
DROP_COLUMNS = {"Time_abs", "Time_rel", "Time", "Compressor Filter Loss", "Turbine Back Pressure"}


def prepare_xy(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    if "source_file" not in df:
        raise ValueError("Processed dataset must retain source_file for group-aware splitting.")
    y = pd.to_numeric(df[target], errors="raise").astype(int)
    groups = df["source_file"].astype(str)
    excluded = TARGET_COLUMNS | METADATA_COLUMNS | DROP_COLUMNS
    candidate = df.drop(columns=[c for c in excluded if c in df.columns])
    X = candidate.select_dtypes(include=["number"]).replace([np.inf, -np.inf], np.nan)
    X = X.loc[:, X.notna().any(axis=0)]
    if X.empty:
        raise ValueError("No numeric model features found in processed dataset.")
    return X, y, groups


def grouped_holdout(X: pd.DataFrame, y: pd.Series, groups: pd.Series):
    labels = set(y.unique())
    # Classification groups contain a single fault label. Hold out one complete
    # source file per class, while retaining at least one training file per class.
    group_labels = pd.DataFrame({"group": groups, "label": y}).groupby("group")["label"].agg(
        lambda values: set(values.unique())
    )
    if all(len(values) == 1 for values in group_labels):
        rng = np.random.default_rng(42)
        held_out = []
        for label in sorted(labels):
            candidates = [group for group, values in group_labels.items() if label in values]
            if len(candidates) < 2:
                raise ValueError(f"Need at least two independent source files for class {label}.")
            held_out.append(rng.permutation(candidates)[0])
        test_mask = groups.isin(held_out).to_numpy()
        return np.flatnonzero(~test_mask), np.flatnonzero(test_mask)

    # Detection files can contain both healthy and anomalous periods. Try
    # deterministic group holdouts until both labels occur on both sides.
    splitter = GroupShuffleSplit(n_splits=100, test_size=0.2, random_state=42)
    for train_idx, test_idx in splitter.split(X, y, groups):
        if set(y.iloc[train_idx].unique()) == labels and set(y.iloc[test_idx].unique()) == labels:
            return train_idx, test_idx
    raise ValueError("Could not form a group-disjoint holdout containing every target class.")


def fit_and_package(df: pd.DataFrame, target: str, name: str, classes: dict[int, str]):
    X, y, groups = prepare_xy(df, target)
    train_idx, test_idx = grouped_holdout(X, y, groups)
    medians = X.iloc[train_idx].median().fillna(0.0)
    X_train = X.iloc[train_idx].fillna(medians)
    X_test = X.iloc[test_idx].fillna(medians)

    model = LGBMClassifier(
        n_estimators=250,
        learning_rate=0.04,
        num_leaves=31,
        class_weight="balanced",
        random_state=42,
        verbosity=-1,
    )
    model.fit(X_train, y.iloc[train_idx])
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)
    metrics = evaluate_classification(y.iloc[test_idx], predictions, probabilities)
    metrics["classification_report"] = classification_report(
        y.iloc[test_idx], predictions, output_dict=True, zero_division=0
    )
    metrics["holdout_groups"] = sorted(groups.iloc[test_idx].unique().tolist())
    metrics["train_groups"] = sorted(groups.iloc[train_idx].unique().tolist())

    package = {
        "model": model,
        "features": X.columns.tolist(),
        "imputation_values": {key: float(value) for key, value in medians.items()},
        "metrics": metrics,
        "classes": {int(key): value for key, value in classes.items()},
    }
    return package, X, y, train_idx


def train_and_export_models():
    if not DETECTION_DATA.exists() or not CLASSIFICATION_DATA.exists():
        raise FileNotFoundError("Run `python -m src.data.loader` to create processed datasets first.")
    MODEL_DIR.joinpath("detection").mkdir(parents=True, exist_ok=True)
    MODEL_DIR.joinpath("classification").mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    detection = pd.read_parquet(DETECTION_DATA)
    classification = pd.read_parquet(CLASSIFICATION_DATA)
    detection_classes = {0: "Normal Operation", 1: "Anomaly"}
    class_names = {
        int(code): FAULT_DISPLAY_NAMES[fault_type]
        for fault_type, code in FAULT_CLASS_MAP.items()
    }

    detector, detection_X, detection_y, detection_train_idx = fit_and_package(
        detection, "anomaly_target", "detection", detection_classes
    )
    classifier, classification_X, classification_y, classification_train_idx = fit_and_package(
        classification, "fault_class", "classification", class_names
    )

    # Store representative training observations for the demo buttons. Choose
    # prototypes that both fitted models recognize as their intended scenario.
    detector_train_X = detection_X.iloc[detection_train_idx].fillna(
        pd.Series(detector["imputation_values"])
    )
    detector_train_y = detection_y.iloc[detection_train_idx]
    normal_candidates = detector_train_X.loc[detector_train_y == 0]
    normal_scores = detector["model"].predict_proba(normal_candidates)[:, list(detector["model"].classes_).index(1)]
    detector["simulation_profiles"] = {
        "normal": normal_candidates.iloc[int(np.argmin(normal_scores))].to_dict()
    }
    classifier["simulation_profiles"] = {}
    classifier_train_df = classification.iloc[classification_train_idx]
    classifier_train_X = classification_X.iloc[classification_train_idx].fillna(
        pd.Series(classifier["imputation_values"])
    )
    class_codes = [int(value) for value in classifier["model"].classes_]
    detector_class_col = list(detector["model"].classes_).index(1)
    for code, display_name in class_names.items():
        candidate_mask = classifier_train_df["fault_class"].to_numpy() == code
        candidates = classifier_train_X.loc[candidate_mask]
        class_col = class_codes.index(code)
        fault_scores = classifier["model"].predict_proba(candidates)[:, class_col]
        anomaly_scores = detector["model"].predict_proba(candidates)[:, detector_class_col]
        fits = (
            (classifier["model"].predict(candidates) == code)
            & (detector["model"].predict(candidates) == 1)
        )
        eligible = np.flatnonzero(fits) if fits.any() else np.arange(len(candidates))
        best = eligible[int(np.argmax((fault_scores * anomaly_scores)[eligible]))]
        classifier["simulation_profiles"][str(code)] = candidates.iloc[int(best)].to_dict()

    artifacts = [
        (MODEL_DIR / "detection" / "marine_fault_detector.joblib", detector),
        (MODEL_DIR / "classification" / "marine_fault_classifier.joblib", classifier),
    ]
    for path, package in artifacts:
        temp_path = path.with_suffix(path.suffix + ".tmp")
        joblib.dump(package, temp_path)
        os.replace(temp_path, path)

    report = {
        "detection": detector["metrics"],
        "classification": classifier["metrics"],
        "features": detector["features"],
        "fault_classes": class_names,
    }
    (RESULT_DIR / "grouped_model_metrics.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print("Models trained and exported with source-file-disjoint holdout metrics.")
    print("Detection:", detector["metrics"]["accuracy"], detector["metrics"]["f1_score"])
    print("Classification:", classifier["metrics"]["accuracy"], classifier["metrics"]["f1_score"])


if __name__ == "__main__":
    train_and_export_models()
