"""Project-wide settings.

Change values here instead of hard-coding them inside chart files.
"""

from pathlib import Path

# --- File paths -------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

# The original file we downloaded from Kaggle. We never edit it by hand.
RAW_DATA_FILE = DATA_DIR / "raw" / "Global_Superstore2.csv"

# The raw file is not UTF-8 (it has characters like "ö"), so it must be read as latin-1.
RAW_DATA_ENCODING = "latin-1"

# The cleaned file created by `python -m scripts.preprocess`. The app reads this one.
PROCESSED_DATA_FILE = DATA_DIR / "processed" / "superstore_clean.csv"

# --- App texts --------------------------------------------------------------
APP_TITLE = "Global Superstore Sales Dashboard"
APP_SUBTITLE = "CEN445 Introduction to Data Visualization - Team Project"

# --- Column settings --------------------------------------------------------
# Columns with dates. They are converted to datetime when the data is loaded.
DATE_COLUMNS = ["Order Date", "Ship Date"]

# Date column used by the date range slider in the sidebar.
DATE_FILTER_COLUMN = "Order Date"

# Categorical columns shown as multiselect filters in the sidebar.
CATEGORY_FILTER_COLUMNS = ["Market", "Category", "Segment"]

# Numeric column used by the "hide outliers" checkbox in the sidebar.
OUTLIER_COLUMN = "Sales"
