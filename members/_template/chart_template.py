"""Chart template - copy this file into your own folder and rename it (e.g. chart_sankey.py).

Every chart file must have:
    TITLE      - short title of the chart
    INSIGHT    - one sentence: what does this chart tell us?
    render(df) - draws the chart. `df` is already filtered by the sidebar.

Rules:
    - Start every widget key with your username, so keys never clash with other members.
    - Use colors from dashboard.theme and call style_figure() on your figure.
    - Always set the chart title, axis labels and legend title.
"""

import plotly.express as px
import streamlit as st

from dashboard.theme import style_figure

TITLE = "Example: distribution of a numeric column"
INSIGHT = "Replace this sentence with the insight your chart shows."

KEY_PREFIX = "template_"  # change to your username, e.g. "reshadverse_"


def render(df):
    numeric_columns = df.select_dtypes("number").columns.tolist()
    if not numeric_columns:
        st.info("There are no numeric columns to plot.")
        return

    # A chart-specific control. Note the key starts with KEY_PREFIX.
    column = st.selectbox("Column", numeric_columns, key=KEY_PREFIX + "column")

    fig = px.histogram(df, x=column, nbins=40, title=TITLE)
    fig.update_layout(xaxis_title=column, yaxis_title="Number of rows")
    fig = style_figure(fig)

    st.plotly_chart(fig)
