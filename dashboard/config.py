"""Project-wide settings.

Change values here instead of hard-coding them inside chart files.
The column settings are filled in after the team agrees on the dataset.
"""

from pathlib import Path

# --- File paths -------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

# The original file we downloaded. We never edit it by hand.
RAW_DATA_FILE = DATA_DIR / "raw" / "dataset.csv"

# The cleaned file created by `python -m scripts.preprocess`. The app reads this one.
PROCESSED_DATA_FILE = DATA_DIR / "processed" / "dataset_clean.csv"

# --- App texts --------------------------------------------------------------
APP_TITLE = "Exploratory Data Visualization Dashboard"
APP_SUBTITLE = "CEN445 Introduction to Data Visualization - Team Project"

# --- Column settings (TODO: fill in after the dataset decision) ------------
# Column with dates. It is converted to datetime when the data is loaded.
DATE_COLUMN = None

# Categorical columns shown as multiselect filters in the sidebar.
CATEGORY_FILTER_COLUMNS = []

# Numeric column used by the "hide outliers" checkbox in the sidebar.
OUTLIER_COLUMN = None
