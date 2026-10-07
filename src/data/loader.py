from __future__ import annotations

from pathlib import Path
import re

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Marine_Engine_Fault_Data"
)

METADATA_DIR = PROJECT_ROOT / "data" / "metadata"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

DATASET_INDEX_PATH = METADATA_DIR / "dataset_index.csv"
VARIABLE_DICTIONARY_PATH = (
    RAW_DATA_DIR / "variable_dictionary.csv"
)

DETECTION_DATASET_PATH = (
    PROCESSED_DIR / "detection_dataset.parquet"
)

CLASSIFICATION_DATASET_PATH = (
    PROCESSED_DIR / "classification_dataset.parquet"
)


# ============================================================
# DATASET CONSTANTS
# ============================================================

REFERENCE_FILE = "Reference_Data.csv"

TARGET_COLUMN = "Anomaly State"

DROP_FEATURE_COLUMNS = {
    "Time_abs",
    "Time_rel",
    "Compressor Filter Loss",
    "Turbine Back Pressure",
}


# ============================================================
# FAULT NAME MAPPING
# ============================================================

FAULT_TYPE_MAP = {
    "air_filter_clogging": [
        "af_clogging",
        "air_filter",
        "air-filter",
        "air filter",
    ],
    "air_cooler_fouling": [
        "ac_fouling",
        "air_cooler",
        "air-cooler",
        "air cooler",
    ],
    "injection_valve_nozzle_clogging": [
        "injector_nozzle",
        "injector nozzle",
        "injection_valve",
        "injection-valve",
        "injection valve",
        "injector",
    ],
    "cooling_water_pump_cavitation": [
        "pump_cavitation",
        "pump cavitation",
        "cooling_water",
        "cooling-water",
        "cooling water",
        "cavitation",
    ],
    "turbine_degradation": [
        "turbine_degradation",
        "turbine degradation",
    ],
}


FAULT_CLASS_MAP = {
    "air_filter_clogging": 0,
    "air_cooler_fouling": 1,
    "injection_valve_nozzle_clogging": 2,
    "cooling_water_pump_cavitation": 3,
    "turbine_degradation": 4,
}


FAULT_DISPLAY_NAMES = {
    "air_filter_clogging": "Air-filter clogging",
    "air_cooler_fouling": "Air-cooler fouling",
    "injection_valve_nozzle_clogging": (
        "Injection-valve nozzle clogging"
    ),
    "cooling_water_pump_cavitation": (
        "Cooling-water pump cavitation"
    ),
    "turbine_degradation": "Turbine degradation",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_filename(filename: str) -> str:
    """
    Normalize filename for robust fault-type matching.
    """

    name = Path(filename).stem.lower()

    name = re.sub(r"[_\-]+", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def infer_fault_type(filename: str) -> str:
    """
    Infer one of the five actual fault types from a
    scenario filename.
    """

    normalized = normalize_filename(filename)

    for fault_type, keywords in FAULT_TYPE_MAP.items():

        for keyword in keywords:

            keyword_normalized = (
                keyword.lower()
                .replace("_", " ")
                .replace("-", " ")
            )

            if keyword_normalized in normalized:
                return fault_type

    return "unknown"


def is_reference_file(filename: str) -> bool:
    """
    Identify the healthy reference dataset.
    """

    return Path(filename).name.lower() == (
        REFERENCE_FILE.lower()
    )


def clean_column_names(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize column names without changing their meaning.
    """

    df = df.copy()

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


def convert_numeric_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert columns that should be numeric.

    This does NOT replace 999 or any other numeric value.
    """

    df = df.copy()

    for column in df.columns:

        if column in {
            "Time_abs",
            "Time_rel",
            "source_file",
            "dataset_type",
            "fault_type",
            "fault_name",
        }:
            continue

        converted = pd.to_numeric(
            df[column],
            errors="coerce",
        )

        # Only replace the original column if conversion
        # produced a meaningful numeric representation.
        if converted.notna().sum() > 0:
            df[column] = converted

    return df


# ============================================================
# DISCOVER CSV FILES
# ============================================================

def discover_csv_files() -> list[Path]:
    """
    Find actual engine-data CSV files.

    Metadata CSV files are excluded.
    """

    if not RAW_DATA_DIR.exists():

        raise FileNotFoundError(
            f"Dataset directory not found:\n"
            f"{RAW_DATA_DIR}"
        )

    csv_files = sorted(
        path
        for path in RAW_DATA_DIR.rglob("*.csv")
        if path.name not in {
            "dataset_index.csv",
            "variable_dictionary.csv",
        }
    )

    if not csv_files:

        raise FileNotFoundError(
            f"No engine-data CSV files found inside:\n"
            f"{RAW_DATA_DIR}"
        )

    return csv_files


# ============================================================
# BUILD DATASET INDEX
# ============================================================

def build_dataset_index() -> pd.DataFrame:
    """
    Scan actual engine-data CSV files and create
    dataset metadata/index.
    """

    csv_files = discover_csv_files()

    records = []

    for csv_path in csv_files:

        try:

            df = pd.read_csv(
                csv_path,
                low_memory=False,
            )

            df = clean_column_names(df)

            row_count = len(df)
            column_count = len(df.columns)

            columns = list(df.columns)

            reference = is_reference_file(
                csv_path.name
            )

            if reference:

                dataset_type = "reference"
                fault_type = "healthy_reference"

            else:

                dataset_type = "scenario"
                fault_type = infer_fault_type(
                    csv_path.name
                )

            if TARGET_COLUMN in df.columns:

                anomaly_state = pd.to_numeric(
                    df[TARGET_COLUMN],
                    errors="coerce",
                )

                pre_anomaly_count = int(
                    (anomaly_state == 0).sum()
                )

                anomaly_count = int(
                    (anomaly_state == 1).sum()
                )

                missing_target_count = int(
                    anomaly_state.isna().sum()
                )

            else:

                pre_anomaly_count = 0
                anomaly_count = 0
                missing_target_count = 0

            records.append(
                {
                    "file_name": csv_path.name,
                    "relative_path": str(
                        csv_path.relative_to(
                            PROJECT_ROOT
                        )
                    ),
                    "dataset_type": dataset_type,
                    "fault_type": fault_type,
                    "rows": row_count,
                    "columns": column_count,
                    "has_anomaly_state": (
                        TARGET_COLUMN in df.columns
                    ),
                    "pre_anomaly_rows": (
                        pre_anomaly_count
                    ),
                    "anomaly_rows": (
                        anomaly_count
                    ),
                    "missing_target_rows": (
                        missing_target_count
                    ),
                    "missing_cells": int(
                        df.isna().sum().sum()
                    ),
                    "column_names": " | ".join(
                        columns
                    ),
                }
            )

        except Exception as exc:

            records.append(
                {
                    "file_name": csv_path.name,
                    "relative_path": str(
                        csv_path.relative_to(
                            PROJECT_ROOT
                        )
                    ),
                    "dataset_type": "error",
                    "fault_type": "unknown",
                    "rows": 0,
                    "columns": 0,
                    "has_anomaly_state": False,
                    "pre_anomaly_rows": 0,
                    "anomaly_rows": 0,
                    "missing_target_rows": 0,
                    "missing_cells": 0,
                    "column_names": "",
                }
            )

            print(
                f"[WARNING] Could not inspect "
                f"{csv_path.name}: {exc}"
            )

    index_df = pd.DataFrame(records)

    METADATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    index_df.to_csv(
        DATASET_INDEX_PATH,
        index=False,
    )

    return index_df


# ============================================================
# LOAD SINGLE CSV
# ============================================================

def load_csv(
    csv_path: Path,
) -> pd.DataFrame:
    """
    Load one actual dataset CSV.

    Reference data:
        Healthy

    Scenario data:
        Uses Anomaly State.

    Missing Anomaly State rows are preserved as NaN
    and removed later when constructing supervised datasets.
    """

    df = pd.read_csv(
        csv_path,
        low_memory=False,
    )

    df = clean_column_names(df)

    df = convert_numeric_columns(df)

    reference = is_reference_file(
        csv_path.name
    )

    if reference:

        dataset_type = "reference"
        fault_type = "healthy_reference"

    else:

        dataset_type = "scenario"

        fault_type = infer_fault_type(
            csv_path.name
        )

        if TARGET_COLUMN not in df.columns:

            raise ValueError(
                f"Scenario file does not contain "
                f"'{TARGET_COLUMN}': "
                f"{csv_path.name}"
            )

    # --------------------------------------------------------
    # Source / experiment metadata
    # --------------------------------------------------------

    df["source_file"] = csv_path.name

    df["dataset_type"] = dataset_type

    df["fault_type"] = fault_type

    # --------------------------------------------------------
    # Anomaly target
    # --------------------------------------------------------

    if reference:

        df["anomaly_target"] = 0

    else:

        df["anomaly_target"] = pd.to_numeric(
            df[TARGET_COLUMN],
            errors="coerce",
        )

    return df


# ============================================================
# LOAD COMPLETE RAW DATASET
# ============================================================

def load_all_data() -> pd.DataFrame:
    """
    Load all actual engine-data CSV files.

    source_file is retained as the experiment/group ID.
    """

    csv_files = discover_csv_files()

    dataframes = []

    for csv_path in csv_files:

        print(
            f"[LOAD] {csv_path.name}"
        )

        df = load_csv(csv_path)

        dataframes.append(df)

    combined = pd.concat(
        dataframes,
        ignore_index=True,
    )

    return combined


# ============================================================
# FEATURE CLEANING
# ============================================================

def prepare_model_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Prepare common model feature columns.

    Removed from primary modeling:
        - Time_abs
        - Time_rel
        - Compressor Filter Loss
        - Turbine Back Pressure
        - Anomaly State
        - anomaly_target
        - fault metadata

    No blanket 999 replacement is performed.
    """

    df = df.copy()

    columns_to_drop = set(
        DROP_FEATURE_COLUMNS
    )

    columns_to_drop.update(
        {
            TARGET_COLUMN,
            "anomaly_target",
            "fault_type",
            "source_file",
            "dataset_type",
            "fault_name",
            "fault_class",
        }
    )

    existing_columns = [
        column
        for column in columns_to_drop
        if column in df.columns
    ]

    return df.drop(
        columns=existing_columns
    )


# ============================================================
# BUILD DETECTION DATASET
# ============================================================

def build_detection_dataset(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build binary Healthy vs Anomaly dataset.

    Healthy:
        Reference_Data rows
        +
        scenario rows with Anomaly State == 0

    Anomaly:
        scenario rows with Anomaly State == 1

    Rows with missing Anomaly State are excluded.
    """

    detection = df.copy()

    detection["anomaly_target"] = pd.to_numeric(
        detection["anomaly_target"],
        errors="coerce",
    )

    detection = detection[
        detection["anomaly_target"].isin(
            [0, 1]
        )
    ].copy()

    detection["anomaly_target"] = (
        detection["anomaly_target"]
        .astype("int8")
    )

    detection["target_name"] = (
        detection["anomaly_target"]
        .map(
            {
                0: "Healthy",
                1: "Anomaly",
            }
        )
    )

    return detection


# ============================================================
# BUILD CLASSIFICATION DATASET
# ============================================================

def build_classification_dataset(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build five-class fault classification dataset.

    Only anomaly rows are included.

    Classes:
        0 Air-filter clogging
        1 Air-cooler fouling
        2 Injection-valve nozzle clogging
        3 Cooling-water pump cavitation
        4 Turbine degradation
    """

    classification = df.copy()

    classification["anomaly_target"] = pd.to_numeric(
        classification["anomaly_target"],
        errors="coerce",
    )

    # Only confirmed anomaly rows.
    classification = classification[
        classification["anomaly_target"] == 1
    ].copy()

    classification["fault_class"] = (
        classification["fault_type"]
        .map(FAULT_CLASS_MAP)
    )

    unknown_mask = (
        classification["fault_class"].isna()
    )

    if unknown_mask.any():

        unknown_files = (
            classification.loc[
                unknown_mask,
                "source_file",
            ]
            .drop_duplicates()
            .tolist()
        )

        raise ValueError(
            "Unknown fault type found in "
            "classification dataset:\n"
            + "\n".join(unknown_files)
        )

    classification["fault_class"] = (
        classification["fault_class"]
        .astype("int8")
    )

    classification["fault_name"] = (
        classification["fault_type"]
        .map(FAULT_DISPLAY_NAMES)
    )

    return classification


# ============================================================
# SAVE PROCESSED DATASETS
# ============================================================

def save_processed_datasets(
    raw_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build and save detection and classification datasets.

    Raw metadata columns are retained so that experiment-aware
    splitting can be performed later.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    detection = build_detection_dataset(
        raw_df
    )

    classification = (
        build_classification_dataset(
            raw_df
        )
    )

    detection.to_parquet(
        DETECTION_DATASET_PATH,
        index=False,
    )

    classification.to_parquet(
        CLASSIFICATION_DATASET_PATH,
        index=False,
    )

    return detection, classification


# ============================================================
# DATASET SUMMARY
# ============================================================

def print_dataset_summary(
    df: pd.DataFrame,
) -> None:

    print("\n" + "=" * 70)
    print(
        "MARINE ENGINE FAULT DATASET SUMMARY"
    )
    print("=" * 70)

    print(
        f"Total rows       : {len(df):,}"
    )

    print(
        f"Total columns    : {len(df.columns):,}"
    )

    print("\nDataset type:")

    print(
        df["dataset_type"]
        .value_counts(dropna=False)
    )

    print("\nFault type:")

    print(
        df["fault_type"]
        .value_counts(dropna=False)
    )

    print("\nAnomaly target:")

    print(
        df["anomaly_target"]
        .value_counts(
            dropna=False
        )
        .sort_index()
    )

    print("\nExperiments / files:")

    print(
        df["source_file"].nunique()
    )

    print("\nMissing values:")

    missing = (
        df.isna()
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        missing[
            missing > 0
        ].head(20)
    )

    print("=" * 70)


def print_processed_summary(
    detection: pd.DataFrame,
    classification: pd.DataFrame,
) -> None:

    print("\n" + "=" * 70)
    print("PROCESSED DATASET SUMMARY")
    print("=" * 70)

    print("\nDetection dataset:")
    print(
        f"Rows: {len(detection):,}"
    )

    print(
        f"Groups: "
        f"{detection['source_file'].nunique()}"
    )

    print(
        detection["anomaly_target"]
        .value_counts()
        .sort_index()
        .rename(
            {
                0: "Healthy",
                1: "Anomaly",
            }
        )
    )

    print("\nClassification dataset:")
    print(
        f"Rows: {len(classification):,}"
    )

    print(
        f"Groups: "
        f"{classification['source_file'].nunique()}"
    )

    print(
        classification[
            [
                "fault_class",
                "fault_name",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            "fault_class"
        )
        .to_string(
            index=False
        )
    )

    print("\nClass distribution:")

    print(
        classification["fault_class"]
        .value_counts()
        .sort_index()
    )

    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "\nMarine Engine Fault ML"
    )

    print(
        "Actual Dataset Loader"
    )

    print("-" * 70)

    print(
        f"Dataset directory:\n"
        f"{RAW_DATA_DIR}\n"
    )

    # --------------------------------------------------------
    # 1. Build metadata index
    # --------------------------------------------------------

    index_df = build_dataset_index()

    print(
        "\nDataset index created:"
    )

    print(
        DATASET_INDEX_PATH
    )

    print("\nFiles discovered:")

    print(
        index_df[
            [
                "file_name",
                "dataset_type",
                "fault_type",
                "rows",
                "columns",
                "pre_anomaly_rows",
                "anomaly_rows",
                "missing_target_rows",
                "missing_cells",
            ]
        ].to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # 2. Load raw data
    # --------------------------------------------------------

    df = load_all_data()

    print_dataset_summary(
        df
    )

    # --------------------------------------------------------
    # 3. Build processed datasets
    # --------------------------------------------------------

    detection, classification = (
        save_processed_datasets(
            df
        )
    )

    print_processed_summary(
        detection,
        classification,
    )

    # --------------------------------------------------------
    # 4. Final paths
    # --------------------------------------------------------

    print("\nSaved processed datasets:")

    print(
        f"Detection:\n"
        f"{DETECTION_DATASET_PATH}"
    )

    print(
        f"Classification:\n"
        f"{CLASSIFICATION_DATASET_PATH}"
    )

    print("\nDONE.")
