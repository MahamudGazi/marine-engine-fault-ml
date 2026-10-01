import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

def evaluate_classification(y_true, y_pred, y_prob=None, average="weighted"):
    """
    Computes comprehensive classification metrics.
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average=average, zero_division=0)
    rec = recall_score(y_true, y_pred, average=average, zero_division=0)
    f1 = f1_score(y_true, y_pred, average=average, zero_division=0)
    
    results = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1)
    }
    
    if y_prob is not None:
        try:
            if len(np.unique(y_true)) == 2:
                # Binary classification
                auc = roc_auc_score(y_true, y_prob[:, 1] if y_prob.ndim == 2 else y_prob)
            else:
                # Multi-class
                auc = roc_auc_score(y_true, y_prob, multi_class="ovr", average=average)
            results["roc_auc"] = float(auc)
        except Exception:
            results["roc_auc"] = None

    results["confusion_matrix"] = confusion_matrix(y_true, y_pred).tolist()
    return results
