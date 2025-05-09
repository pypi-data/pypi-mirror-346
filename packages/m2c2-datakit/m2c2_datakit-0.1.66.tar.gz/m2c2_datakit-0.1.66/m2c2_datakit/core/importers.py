import glob
import json
import requests
from abc import ABC, abstractmethod
from .config import settings
from pathlib import Path
from .log import log_info, log_error
from .utils import get_filename_timestamp
import pandas as pd
from .helpers import (
    parse_json_to_dfs,
    verify_dataframe_parsing,
    unnest_trial_level_data,
)

# from .codebook import make_codebook
# from .plot import plot_distribution, plot_pairplot  # optionally import inside method


# === Importer Classes ===
class BaseImporter(ABC):
    @abstractmethod
    def load(self, source_path: str):
        pass

    def _process(self, df: pd.DataFrame, activity_name_col: str):
        grouped = parse_json_to_dfs(df, activity_name_col)
        validation, activity_names = verify_dataframe_parsing(
            df, grouped, activity_name_col
        )
        return df, grouped, validation, activity_names, get_filename_timestamp()


class MetricWireImporter(BaseImporter):
    def load(self, filepath: str = "metricwire/data/unzipped/*/*/*.json"):
        json_files = glob.glob(filepath)
        log_info("Found MetricWire JSON files", {"count": len(json_files)})

        data = [json.load(open(fp)) for fp in json_files]
        flattened = [
            {**{k: v for k, v in record.items() if k != "data"}, **entry}
            for record_list in data
            for record in record_list
            for entry in record.get("data", [])
        ]
        return self._process(pd.DataFrame(flattened), activity_name_col="activityName")


class MongoDBImporter(BaseImporter):
    def load(self, source_path: str):
        df_flat = pd.read_json(source_path)
        return self._process(df_flat, activity_name_col="activity_name")

    def _process(self, df: pd.DataFrame, activity_name_col: str):
        grouped = parse_json_to_dfs(df, activity_name_col)
        # for each grouped dataset, apply unnest
        for name, group in grouped.items():
            grouped[name] = unnest_trial_level_data(group, drop_duplicates=True)
        validation, activity_names = verify_dataframe_parsing(
            df, grouped, activity_name_col
        )
        return df, grouped, validation, activity_names, get_filename_timestamp()


class UASImporter(BaseImporter):
    def load(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            log_error("Failed to fetch UAS data", {"error": str(e)})
            return pd.DataFrame(), {}, False, []

        lines = [
            line.strip().rstrip(",")
            for line in response.text.splitlines()
            if line.strip()
        ]
        parsed = [json.loads(line) for line in lines if line]
        df = pd.DataFrame(parsed)

        if "data" not in df.columns:
            raise ValueError("Expected 'data' column not found in UAS export.")

        expanded = df["data"].apply(pd.Series)
        full_df = pd.concat([df.drop(columns=["data"]), expanded], axis=1)
        return self._process(full_df, activity_name_col="taskname")


class QualtricsImporter(BaseImporter):
    def load(self, source_path: str):
        df = pd.read_csv(source_path, header=1, skiprows=[2])
        return self._process(df)


class MultiCSVImporter(BaseImporter):
    def load(self, source_map: dict, activity_name_col: str = "activity_name"):
        """
        Load and stack multiple CSV files tagged with activity names.

        Args:
            source_map (dict): Mapping from activity name to file path.
            key_name (str): Column to tag source of each row (e.g., "activity_name").

        Returns:
            pd.DataFrame: Combined dataframe with all sources stacked.
        """
        dfs = []
        for activity, path in source_map.items():
            df = pd.read_csv(Path(path))
            df[activity_name_col] = activity
            dfs.append(df)

        combined_df = pd.concat(dfs, ignore_index=True)
        return self._process(combined_df, activity_name_col=activity_name_col)

class DataImporter:
    SOURCES = {
        "metricwire": MetricWireImporter,
        "mongodb": MongoDBImporter,
        "uas": UASImporter,
        "multicsv": MultiCSVImporter,
    }

    @staticmethod
    def load_from(source_name: str, source_path: str):
        name = source_name.lower()
        if name not in DataImporter.SOURCES:
            log_error("Unsupported source", {"source_name": source_name})
            raise ValueError(f"Unsupported source: '{source_name}'")

        log_info("Initializing data load", {"source": source_name, "path": source_path})
        return DataImporter.SOURCES[name]().load(source_path)
