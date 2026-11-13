"""Heatmap chart (B3): profitability and sales matrix across sub-categories and markets."""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.theme import DIVERGING_SCALE, SEQUENTIAL_SCALE, style_figure

TITLE = "Profitability Matrix by Sub-Category and Market"
INSIGHT = (
    "Tables generate severe losses across nearly every major market (especially APAC, EU, "
    "and LATAM), whereas Copiers, Phones, and Chairs consistently deliver the highest profit."
)

KEY_PREFIX = "reshadverse_heatmap_"

METRICS = [
    "Total Profit (USD)",
    "Profit Margin (%)",
    "Total Sales (USD)",
]


def _build_matrix(df: pd.DataFrame, col_dim: str, metric: str) -> pd.DataFrame:
    """Build a sorted pivot matrix with Sub-Category as rows and Market/Region as columns."""
    grouped = df.groupby(["Sub-Category", col_dim], as_index=False).agg(
        Profit=("Profit", "sum"),
        Sales=("Sales", "sum"),
    )

    if metric == "Total Profit (USD)":
        grouped["Value"] = grouped["Profit"]
    elif metric == "Profit Margin (%)":
        grouped["Value"] = (grouped["Profit"] / grouped["Sales"].replace(0, float("nan"))) * 100.0
    else:
        grouped["Value"] = grouped["Sales"]

    matrix = grouped.pivot(index="Sub-Category", columns=col_dim, values="Value").fillna(0.0)

    row_order = matrix.sum(axis=1).sort_values(ascending=False).index
    col_order = matrix.sum(axis=0).sort_values(ascending=False).index
    return matrix.loc[row_order, col_order]


def render(df: pd.DataFrame):
    """Render the interactive Sub-Category x Market/Region heatmap."""
    if df.empty:
        st.info("No data available for the selected filters.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        metric = st.selectbox(
            "Metric",
            options=METRICS,
            key=KEY_PREFIX + "metric",
        )
    with col2:
        col_dim = st.selectbox(
            "Geography level (columns)",
            options=["Market", "Region"],
            key=KEY_PREFIX + "coldim",
        )
    with col3:
        show_values = st.checkbox(
            "Show numbers inside cells",
            value=True,
            key=KEY_PREFIX + "values",
        )

    matrix = _build_matrix(df, col_dim, metric)

    if metric == "Total Sales (USD)":
        color_kwargs = dict(color_continuous_scale=SEQUENTIAL_SCALE)
    else:
        color_kwargs = dict(
            color_continuous_scale=DIVERGING_SCALE,
            color_continuous_midpoint=0,
        )

    text_format = ".1f" if metric == "Profit Margin (%)" else ",.0f"

    fig = px.imshow(
        matrix,
        aspect="auto",
        text_auto=text_format if show_values else False,
        labels=dict(x=col_dim, y="Sub-Category", color=metric),
        title=f"{TITLE} ({metric} by {col_dim})",
        **color_kwargs,
    )

    value_prefix = "$" if "USD" in metric else ""
    value_suffix = "%" if "%" in metric else ""
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b> in <b>%{x}</b><br>"
            f"{metric}: {value_prefix}%{{z:{text_format}}}{value_suffix}<extra></extra>"
        )
    )
    fig.update_layout(
        xaxis_title=col_dim,
        yaxis_title="Sub-Category",
    )
    fig = style_figure(fig, height=580)

    st.plotly_chart(fig)
