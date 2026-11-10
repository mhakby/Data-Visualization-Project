"""The "Overview" tab: a quick look at the dataset and its quality."""

import pandas as pd
import streamlit as st

from dashboard.preprocessing import missing_value_report


def render_overview(df, filtered_df):
    """Show dataset size, a preview table and a per-column summary."""
    numeric_count = len(df.select_dtypes("number").columns)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows (after filters)", f"{len(filtered_df):,}")
    col2.metric("Columns", df.shape[1])
    col3.metric("Numeric columns", numeric_count)
    col4.metric("Other columns", df.shape[1] - numeric_count)

    st.subheader("Data preview")
    st.dataframe(filtered_df.head(100), hide_index=True)

    st.subheader("Column summary")
    summary = pd.DataFrame(
        {
            "type": df.dtypes.astype(str),
            "unique_values": df.nunique(),
        }
    ).join(missing_value_report(df))
    st.dataframe(summary)
