import pandas as pd
import zipfile
import glob
import json
import datetime
import requests
from typing import Any, Dict, List, Tuple
from abc import ABC, abstractmethod


# ========== 🔧 Utility Functions ==========

def read_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def get_data_from_json_files(json_files):
    data = []
    for file in json_files:
        data.append(read_json_file(file))
    return data

def list_zip_contents(zip_path: str) -> Dict[str, int]:
    """List contents and sizes of files within a zip archive."""
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        return {name: zip_ref.getinfo(name).file_size for name in zip_ref.namelist()}


def read_zip_files(zip_path: str, zip_contents: Dict[str, int]) -> Dict[str, pd.DataFrame]:
    """Read and parse pipe-delimited files from a zip archive into DataFrames."""
    file_data = {}
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_name in zip_contents.keys():
            df = pd.read_csv(file_name, delimiter="|")
            print(df.head())
            file_data[file_name] = df
    return file_data


def parse_json_to_dfs(df: pd.DataFrame, activity_name_col="activity_name") -> Dict[str, pd.DataFrame]:
    """Split a DataFrame into multiple DataFrames based on the activity name column."""
    grouped = df.groupby(activity_name_col)
    return {name: group.reset_index(drop=True) for name, group in grouped}


def verify_dataframe_parsing(
    df: pd.DataFrame,
    grouped_dataframes: Dict[Any, pd.DataFrame],
    activity_name_col="activity_name"
) -> Tuple[bool, Dict[str, set]]:
    """Check whether the grouping of activity names is consistent between original and split DataFrames."""
    parsed_names = set(df[activity_name_col].unique())
    grouped_names = set(grouped_dataframes.keys())

    return parsed_names == grouped_names, {
        "parsed_json": parsed_names,
        "grouped_df": grouped_names
    }

def validate_input(df: Any, required_columns: List[str] = None) -> None:
    """Ensure the input is a DataFrame with required columns."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")


def unnest_trial_level_data(
    df: pd.DataFrame,
    drop_duplicates=True,
    column_order: List[str] = [
        "participant_id", "session_id", "group", "wave", "activity_id",
        "study_id", "document_uuid"
    ]
) -> pd.DataFrame:
    """Unnest trial-level data from a column named 'content'."""
    all_trials = []
    for _, row in df.iterrows():
        trials = row["content"].get("trials", [])
        all_trials.extend(trials)

    trial_df = pd.DataFrame(all_trials)
    reordered_cols = column_order + [col for col in trial_df.columns if col not in column_order]
    trial_df = trial_df[reordered_cols]

    if drop_duplicates:
        trial_df = trial_df.drop_duplicates(
            subset=["activity_uuid", "session_uuid", "trial_begin_iso8601_timestamp"]
        )
    return trial_df

# ========== 🧱 Importer Classes ==========

class BaseImporter(ABC):
    """Abstract base class for all data importers."""

    @abstractmethod
    def load(self, source_path: str):
        pass

    def _process(self, df: pd.DataFrame, activity_name_col: str = "activityName"):
        grouped = parse_json_to_dfs(df, activity_name_col=activity_name_col)
        validation, activity_names = verify_dataframe_parsing(df, grouped, activity_name_col=activity_name_col)
        return df, grouped, validation, activity_names


class MetricWireImporter(BaseImporter):
    """Loader for MetricWire JSON exports."""

    def _read_json_file(self, file_path: str) -> dict:
        with open(file_path) as f:
            return json.load(f)

    def _get_data_from_json_files(self, json_files: List[str]) -> List[dict]:
        return [self._read_json_file(fp) for fp in json_files]

    def load(self, filepath: str = "metricwire/data/unzipped/*/*/*.json"):
        json_files = glob.glob(filepath)
        print(f"Ready to process {len(json_files)} JSON files exported from Metricwire.")

        data = self._get_data_from_json_files(json_files)
        flattened_data = []

        for i in range(len(data)):
            for j in range(len(data[i])):
                print(data[i][j])  # debug
                record = data[i][j]
                identifiers = {k: v for k, v in record.items() if k != "data"}
                for entry in record.get("data", []):
                    flattened_data.append({**identifiers, **entry})

        df = pd.DataFrame(flattened_data)
        return self._process(df, activity_name_col="activityName")


class MongoDBImporter(BaseImporter):
    """Loader for MongoDB-exported JSON files."""

    def load(self, source_path: str):
        df = pd.read_json(source_path)
        grouped_dataframes = parse_json_to_dfs(df)
        validation, activity_names = verify_dataframe_parsing(df, grouped_dataframes)
        return df, grouped_dataframes, validation, activity_names


class UASImporter(BaseImporter):
    """Loader for Understanding America Study (UAS) NDJSON-style exports."""

    def load(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from URL: {e}")
            return pd.DataFrame(), {}, False, []

        raw = response.text
        content_type = response.headers.get("Content-Type", "")

        print("Response is JSON" if 'application/json' in content_type else "Response is not JSON")

        # Parse each JSON line
        lines = raw.splitlines()
        parsed_lines = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            if line.endswith(','):
                line = line.rstrip(',')
            try:
                parsed_lines.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Skipping line {i}: {e}")

        # Build DataFrame
        df = pd.DataFrame(parsed_lines)

        if "data" not in df.columns:
            raise ValueError("Expected 'data' column not found in UAS export.")

        expanded_data = df["data"].apply(pd.Series)
        full_df = pd.concat([df.drop(columns=["data"]), expanded_data], axis=1)

        return self._process(full_df, activity_name_col="taskname")

class DataImporter:
    """User-friendly API to load study data from various sources."""
    
    SOURCES = {
        "metricwire": MetricWireImporter,
        "mongodb": MongoDBImporter,
        "uas": UASImporter
    }

    @staticmethod
    def load_from(source_name: str, source_path: str):
        name = source_name.lower()
        if name not in DataImporter.SOURCES:
            raise ValueError(
                f"Unsupported source: '{source_name}'. Available: {list(DataImporter.SOURCES)}"
            )
        importer = DataImporter.SOURCES[name]()
        return importer.load(source_path)
