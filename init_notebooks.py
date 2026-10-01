import json
import os

notebooks = {
    "01_dataset_inspection.ipynb": "## 01 - Marine Engine Dataset Inspection\nSanity checks, schema inspection, missing values, and engineering units validation.",
    "02_eda.ipynb": "## 02 - Exploratory Data Analysis\nSensor distributions, cylinder exhaust heat maps, and correlation matrices.",
    "03_data_cleaning.ipynb": "## 03 - Data Cleaning & Preprocessing\nSensor noise filtering, physical range clipping, and missing value imputation.",
    "04_feature_engineering.ipynb": "## 04 - Mechanical & Thermodynamic Feature Engineering\nCylinder temperature deviation, turbocharger boost ratios, and thermal efficiency proxies.",
    "05_fault_detection.ipynb": "## 05 - Binary Anomaly Detection Models\nTraining baseline & LightGBM anomaly detection models (Normal vs Fault).",
    "06_fault_classification.ipynb": "## 06 - Multi-Class Fault Diagnosis\nTraining XGBoost / Random Forest for 6 distinct marine engine fault modes.",
    "07_model_comparison.ipynb": "## 07 - Model Benchmarking & Performance Comparison\nPrecision-Recall curves, ROC-AUC, confusion matrices, and inference latency.",
    "08_shap_explainability.ipynb": "## 08 - Explainable AI (XAI) with SHAP\nTreeExplainer, waterfall plots, and global feature importance attributions."
}

for nb_name, title in notebooks.items():
    nb_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# 🚢 {title}\n"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "\n",
                    "# Load processed marine telemetry dataset\n",
                    "df = pd.read_parquet('../data/processed/classification_dataset.parquet')\n",
                    "df.head()\n"
                ]
            }
        ],
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    with open(os.path.join("notebooks", nb_name), "w", encoding="utf-8") as f:
        json.dump(nb_content, f, indent=2)

print("All 8 Jupyter notebooks initialized successfully.")
