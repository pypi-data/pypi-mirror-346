import os
from typing import List
from pydantic import BaseModel, Field
from importlib.metadata import version
from pathlib import Path

# def unnest_trial_level_data(df: pd.DataFrame, drop_duplicates=True, column_order: List[str] = None) -> pd.DataFrame:
#     column_order = column_order or ["participant_id", "session_id", "group", "wave", "activity_id", "study_id", "document_uuid"]
#     trial_df = trial_df.drop_duplicates(subset=["activity_uuid", "session_uuid", "trial_begin_iso8601_timestamp"])

<<<<<<< HEAD

class Settings(BaseModel):
    PACKAGE_VERSION: str = Field(default_factory=lambda: version("m2c2-datakit"))

    # ABSTRACT ALL IDS BY PROVIDER
    DEDUP_IDS_METRICWIRE: List[str] = [
        "userId",
        "submissionSessionId",
        "activityId",
    ]
    DEDUP_IDS_UAS: List[str] = [
        "userId",
        "submissionSessionId",
        "activityId",
    ]
    
    DEDUP_IDS_MONGODB: List[str] = []
    DEDUP_IDS_QUALTRICS: List[str] = ["index", "ResponseId", 'M2C2_ASSESSMENT_ORDER', 'M2C2_AUTO_ADVANCE', 'M2C2_LANGUAGE']

    STANDARD_GROUPING_FOR_AGGREGATION: List[str] = [
        "study_uid",
        "user_uid",
        "uuid",
        "activity_name",
    ]
    STANDARD_GROUPING_FOR_AGGREGATION_QUALTRICS: List[str] = ['ResponseId']
    
    STANDARD_GROUPING_FOR_AGGREGATION_METRICWIRE: List[str] = [
        "userId",
        "submissionSessionId",
        "activityId",
    ]
    STANDARD_GROUPING_FOR_AGGREGATION_UAS: List[str] = [
        "userId",
        "submissionSessionId",
        "activityId",
    ]
    
    @property
    def DEFAULT_FUNC_MAP_SCORING(self):
        from .map import DEFAULT_FUNC_MAP_SCORING
        return DEFAULT_FUNC_MAP_SCORING
    
    # DEFAULTS FOR UI
    DEFAULT_PLOT_COLOR: str = "steelblue"
    DEFAULT_PLOT_DPI: int = 150


settings = Settings()

# === Environment Safeguards ===
os.environ["LOGFIRE_DISABLE_CLOUD"] = "1"
os.environ["LOGFIRE_IGNORE_NO_CONFIG"] = "1"

# === Local JSONL Logging Setup ===
LOG_DIR = Path.cwd() / "logs"
LOG_FILE = LOG_DIR / "events.jsonl"
LOG_DIR.mkdir(exist_ok=True)
=======
# Approach #1: Simple Constants
package_version = package_version
standard_grouping_for_aggregation = ["participant_id", "session_uuid", "session_id"]
standard_grouping_for_aggregation_metricwire = [
    "userId",
    "submissionSessionId",
    "activityId",
]
default_plot_color = "steelblue"
default_plot_dpi = 150


"""Global constants and metadata for the m2c2_datakit package."""

from importlib.metadata import version as get_version
from typing import List
from pydantic import BaseModel, Field

# def unnest_trial_level_data(df: pd.DataFrame, drop_duplicates=True, column_order: List[str] = None) -> pd.DataFrame:
#     """Unnest trial-level data from a 'content' column containing trials."""
#     column_order = column_order or ["participant_id", "session_id", "group", "wave", "activity_id", "study_id", "document_uuid"]
#     trial_df = trial_df.drop_duplicates(subset=["activity_uuid", "session_uuid", "trial_begin_iso8601_timestamp"])
#     return trial_df

# === Constants and Settings ===
class Settings(BaseModel):
    PACKAGE_VERSION: str = Field(default_factory=lambda: get_version("m2c2_datakit"))
    STANDARD_GROUPING_FOR_AGGREGATION: List[str] = [
        "participant_id", "session_uuid", "session_id"
    ]
    STANDARD_GROUPING_FOR_AGGREGATION_METRICWIRE: List[str] = [
        "userId", "submissionSessionId", "activityId"
    ]
    DEFAULT_PLOT_COLOR: str = "steelblue"
    DEFAULT_PLOT_DPI: int = 150

settings = Settings()
>>>>>>> origin/main
