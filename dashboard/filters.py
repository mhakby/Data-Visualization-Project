"""Sidebar filters shared by the whole dashboard.

Every chart receives the DataFrame *after* these filters, so members do not
need to build their own global filters.
"""

import streamlit as st

from dashboard import config
from dashboard.preprocessing import find_outliers_iqr


def sidebar_filters(df):
    """Draw the sidebar widgets and return the filtered DataFrame."""
    st.sidebar.header("Filters")
    filtered = df

    # 1) Multiselect for each categorical column in the config.
    for column in config.CATEGORY_FILTER_COLUMNS:
        options = sorted(df[column].dropna().unique())
        selected = st.sidebar.multiselect(
            column, options, default=options, key=f"filter_{column}"
        )
        filtered = filtered[filtered[column].isin(selected)]

    # 2) Date range slider.
    if config.DATE_FILTER_COLUMN:
        min_date = df[config.DATE_FILTER_COLUMN].min().date()
        max_date = df[config.DATE_FILTER_COLUMN].max().date()
        start_date, end_date = st.sidebar.slider(
            "Date range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            key="filter_date_range",
        )
        dates = filtered[config.DATE_FILTER_COLUMN].dt.date
        filtered = filtered[(dates >= start_date) & (dates <= end_date)]

    # 3) Checkbox to hide outliers.
    if config.OUTLIER_COLUMN:
        hide_outliers = st.sidebar.checkbox(
            f"Hide outliers in {config.OUTLIER_COLUMN}", key="filter_hide_outliers"
        )
        if hide_outliers:
            is_outlier = find_outliers_iqr(df[config.OUTLIER_COLUMN])
            filtered = filtered[~is_outlier.loc[filtered.index]]

    st.sidebar.caption(f"{len(filtered):,} of {len(df):,} rows selected")
    return filtered
