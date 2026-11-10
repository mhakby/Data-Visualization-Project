"""Loads the cleaned dataset for the app."""

import pandas as pd
import streamlit as st

from dashboard import config


# st.cache_data keeps the result in memory, so the CSV is read only once
# instead of on every click in the app.
@st.cache_data
def load_data():
    """Return the cleaned dataset as a DataFrame, or None if the file does not exist yet."""
    if not config.PROCESSED_DATA_FILE.exists():
        return None

    df = pd.read_csv(config.PROCESSED_DATA_FILE)

    # CSV files store dates as text, so we convert them back to datetime.
    if config.DATE_COLUMN:
        df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN])

    return df
