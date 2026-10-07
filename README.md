# Marine Engine Fault Detection

A research and demo project for binary anomaly detection and five-class fault diagnosis using marine engine telemetry. The repository includes processed real-world datasets, source-file-aware training, a Django REST API, and a React dashboard.

## Data and labels

The processed tables are generated from the CSV files under `data/raw/Marine_Engine_Fault_Data/Marine_Engine_Fault_Data/`.

- Detection: `anomaly_target` identifies healthy (`0`) versus anomalous (`1`) records.
- Classification: anomalous records are labeled as air-filter clogging, air-cooler fouling, injection-valve nozzle clogging, cooling-water pump cavitation, or turbine degradation.
- `source_file` is retained as the experiment ID. Training holds out complete source files so adjacent readings from one experiment cannot appear in both train and evaluation data.
- Model inputs use the dataset's numeric sensor columns. Time, targets, labels, source metadata, and the two explicitly excluded columns are not model inputs.

The dashboard's scenario buttons use representative training records selected because the fitted models recognize the intended scenario. These profiles exercise the API; they are not live vessel telemetry or independent measured fault sequences.

## Setup

From the repository root, create and activate a virtual environment, then install the ML/backend dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

Build the processed datasets (if they are absent) and train the models:

```powershell
python -m src.data.loader
python train_models.py
```

Training writes model artifacts to `models/detection/` and `models/classification/`, and grouped holdout metrics to `reports/results/grouped_model_metrics.json`.

Start the backend in one terminal:

```powershell
cd backend
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py runserver
```

Start the dashboard in another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://localhost:8000`. The prediction endpoint expects every numeric feature required by the trained model; use `/api/telemetry/simulate/?scenario=normal` or one of the five fault scenario IDs to get a compatible example payload.

## Main folders

- `src/data/`: raw data discovery, labeling, and processed dataset construction.
- `train_models.py`: source-file-disjoint model training and artifact export.
- `backend/`: Django API, prediction history, and scenario profile endpoint.
- `frontend/`: React engineering dashboard.
- `models/`: trained detector and classifier artifacts.
- `reports/results/`: grouped holdout metrics.

## Limitations

This is a research/demo system. Grouped holdout scores are substantially lower than random-row scores can be, because entire operating runs are held out; check `reports/results/grouped_model_metrics.json` before interpreting a model. Scenario profiles are training records and should not be treated as independent operational examples. Validate the models on independent vessel data and review the Django deployment settings before exposing the service publicly.
