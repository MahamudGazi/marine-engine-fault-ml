# 🚢 Marine Engine Fault Detection & Monitoring System (AI + Mechanical Engineering + Full-Stack)

An end-to-end industrial Machine Learning and telemetry analytics system for Marine Engine Fault Detection, Classification, and Explainable AI (SHAP) with a real-time engineering monitoring dashboard.

---

## 📁 Project Directory Structure

```plaintext
marine-engine-fault-ml/
│
├── data/
│   ├── raw/
│   │   └── Marine_Engine_Fault_Data/        # Original sensor readings & telemetry logs
│   ├── processed/
│   │   ├── detection_dataset.parquet        # Cleaned dataset for binary anomaly detection
│   │   └── classification_dataset.parquet   # Multi-class fault diagnosis dataset
│   └── metadata/
│       ├── dataset_index.csv                # Dataset manifest & run conditions
│       └── variable_dictionary.csv          # Engineering parameters & sensor units
│
├── notebooks/
│   ├── 01_dataset_inspection.ipynb          # Raw dataset sanity checks & validation
│   ├── 02_eda.ipynb                         # Exploratory Data Analysis & sensor correlations
│   ├── 03_data_cleaning.ipynb               # Outlier filtering, imputation, smoothing
│   ├── 04_feature_engineering.ipynb         # Thermodynamic ratios, rolling stats, FFT/vibration
│   ├── 05_fault_detection.ipynb             # Binary fault detection models (Normal vs Anomaly)
│   ├── 06_fault_classification.ipynb        # Multi-class fault diagnosis (Turbine, Injector, etc.)
│   ├── 07_model_comparison.ipynb            # ROC/AUC, F1, latency & benchmarking
│   └── 08_shap_explainability.ipynb         # SHAP TreeExplainer, waterfall & summary plots
│
├── src/
│   ├── data/
│   │   ├── loader.py                        # Parquet/CSV batch & stream loader
│   │   ├── cleaning.py                      # Data validation & cleansing routines
│   │   └── labeling.py                      # Fault taxonomy mapping & label encoding
│   │
│   ├── features/
│   │   ├── selection.py                     # Mutual info, recursive feature elimination
│   │   └── engineering.py                   # Domain-specific thermodynamic & mechanical features
│   │
│   ├── models/
│   │   ├── baseline.py                      # Logistic / Decision Tree baselines
│   │   ├── random_forest.py                 # Random Forest classifier pipeline
│   │   ├── xgboost_model.py                 # XGBoost tuned model pipeline
│   │   └── lightgbm_model.py                # LightGBM tuned model pipeline
│   │
│   ├── evaluation/
│   │   ├── metrics.py                       # Precision, Recall, F1, Confusion Matrix
│   │   ├── splits.py                        # Time-series / Stratified group splits
│   │   └── plots.py                         # PR curves, ROC curves, calibration plots
│   │
│   └── explainability/
│       └── shap_analysis.py                 # Fast inference SHAP feature contribution extractor
│
├── models/
│   ├── detection/                           # Serialized binary anomaly detection models (.joblib)
│   └── classification/                      # Serialized multi-class fault classification models (.joblib)
│
├── backend/
│   └── django_project/                      # Django & Django REST Framework Backend
│       ├── manage.py
│       ├── config/                          # Django settings, ASGI/WSGI, root URLs
│       ├── api/                             # DRF routers and general endpoints
│       ├── predictions/                     # ML inference engine & SHAP explanation services
│       ├── authentication/                  # Token authentication / user management
│       ├── dashboard/                       # Telemetry history, stats & metrics endpoints
│       └── requirements.txt
│
├── frontend/
│   └── react-dashboard/                     # React + Vite Marine Engineering Dashboard
│       ├── src/
│       │   ├── components/                  # Gauges, HUD Status, SHAP Bar, Logs
│       │   ├── services/                    # API client layer
│       │   └── App.jsx
│       ├── public/
│       ├── package.json
│       └── vite.config.js
│
├── reports/
│   ├── figures/                             # High-res confusion matrices, SHAP summary plots
│   ├── tables/                              # Markdown / LaTeX metric comparison tables
│   └── results/                             # Model benchmark JSON logs
│
├── tests/                                   # Unit & integration tests for ML & APIs
├── requirements.txt                         # Root ML & Data Science dependencies
├── README.md                                # Project documentation
└── .gitignore                               # Git ignore rules
```

---

## 🛠️ System Architecture

```
[ Sensor Telemetry / User Input ]
             ↓
 [ React Engineering Dashboard ]
             ↓ (REST API)
    [ Django REST Backend ]
       ├── Auth & History (DB)
       ├── ML Inference Engine (LightGBM / XGBoost)
       └── Explainable AI (SHAP TreeExplainer)
             ↓
[ JSON Response: Status + Fault + Confidence + SHAP Contributions ]
```

---

## 🚀 Getting Started

### 1. ML Environment Setup
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Backend Setup
```bash
cd backend/django_project
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd frontend/react-dashboard
npm install
npm run dev
```
