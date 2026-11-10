"""Main Streamlit application.

Run with:
    streamlit run app.py

Team members do not need to edit this file. Charts are added in members/<username>/.
"""

import streamlit as st

from dashboard import config
from dashboard.data_loader import load_data
from dashboard.filters import sidebar_filters
from dashboard.overview import render_overview
from dashboard.theme import apply_theme
from members import ALL_MEMBERS


def show_member_charts(member, df):
    """Draw every chart listed in a member's CHARTS list."""
    if not member.CHARTS:
        st.info("No charts added yet.")
        return

    for chart in member.CHARTS:
        with st.container(border=True):
            # If one chart has a bug, show the error but keep drawing the other charts.
            try:
                chart.render(df)
            except Exception as error:
                st.error(f"The chart '{chart.TITLE}' could not be drawn.")
                st.exception(error)
            st.caption(f"Insight: {chart.INSIGHT}")


st.set_page_config(page_title=config.APP_TITLE, page_icon="📊", layout="wide")
apply_theme()

st.title(config.APP_TITLE)
st.caption(config.APP_SUBTITLE)

df = load_data()
if df is None:
    st.warning(
        "The cleaned dataset was not found. Put the raw data in `data/raw/` "
        "and run `python -m scripts.preprocess` first."
    )
    st.stop()

filtered_df = sidebar_filters(df)
if filtered_df.empty:
    st.warning("No rows match the selected filters. Try changing the filters in the sidebar.")
    st.stop()

tab_names = ["Overview"] + [member.TAB_TITLE for member in ALL_MEMBERS]
tabs = st.tabs(tab_names)

with tabs[0]:
    render_overview(df, filtered_df)

for tab, member in zip(tabs[1:], ALL_MEMBERS):
    with tab:
        show_member_charts(member, filtered_df)
