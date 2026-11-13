"""Parallel coordinates chart (B2): multivariate view of discount, quantity, shipping and profit."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.theme import DIVERGING_SCALE, style_figure

TITLE = "Multivariate Analysis: Discount, Quantity, Shipping Cost, and Profit"
INSIGHT = (
    "Orders with discounts above 20% almost consistently result in negative profit margins "
    "(red lines), regardless of order quantity or shipping cost."
)

KEY_PREFIX = "reshadverse_parallel_"

MODE_AGGREGATED = "Sub-Category x Segment averages (clean overview)"
MODE_ORDERS = "Individual orders (sampled)"


def _prepare_data(df: pd.DataFrame, mode: str, sample_size: int) -> pd.DataFrame:
    """Prepare either aggregated (Segment x Sub-Category) averages or a sample of orders."""
    work_df = df.copy()
    work_df["Discount_Pct"] = work_df["Discount"] * 100.0
    work_df["Profit_Margin_Pct"] = work_df["Profit Margin"] * 100.0

    if mode == MODE_AGGREGATED:
        grouped = work_df.groupby(["Segment", "Sub-Category"], as_index=False).agg(
            Discount_Pct=("Discount_Pct", "mean"),
            Quantity=("Quantity", "mean"),
            Shipping_Cost=("Shipping Cost", "mean"),
            Sales=("Sales", "mean"),
            Profit=("Profit", "mean"),
            Profit_Margin_Pct=("Profit_Margin_Pct", "mean"),
        )
        return grouped

    work_df = work_df.rename(columns={"Shipping Cost": "Shipping_Cost"})
    if len(work_df) > sample_size:
        return work_df.sample(n=sample_size, random_state=42)
    return work_df


def render(df: pd.DataFrame):
    """Render the interactive Parallel Coordinates chart."""
    if df.empty:
        st.info("No data available for the selected filters.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        mode = st.selectbox(
            "View level",
            options=[MODE_AGGREGATED, MODE_ORDERS],
            key=KEY_PREFIX + "mode",
        )
    with col2:
        color_by = st.selectbox(
            "Color lines by",
            options=["Profit Margin (%)", "Profit (USD)"],
            key=KEY_PREFIX + "color",
        )
    with col3:
        sample_size = st.slider(
            "Max orders (for individual orders mode)",
            min_value=200,
            max_value=3000,
            value=1000,
            step=200,
            disabled=(mode == MODE_AGGREGATED),
            key=KEY_PREFIX + "sample",
        )

    plot_df = _prepare_data(df, mode, sample_size)
    color_col = "Profit_Margin_Pct" if color_by == "Profit Margin (%)" else "Profit"

    max_abs = float(max(abs(plot_df[color_col].min()), abs(plot_df[color_col].max()), 1.0))

    dimensions = [
        dict(label="Discount (%)", values=plot_df["Discount_Pct"], range=[0, 85]),
        dict(label="Quantity", values=plot_df["Quantity"]),
        dict(label="Shipping Cost ($)", values=plot_df["Shipping_Cost"]),
        dict(label="Sales ($)", values=plot_df["Sales"]),
        dict(label="Profit ($)", values=plot_df["Profit"]),
        dict(label="Profit Margin (%)", values=plot_df["Profit_Margin_Pct"]),
    ]

    fig = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=plot_df[color_col],
                colorscale=DIVERGING_SCALE,
                cmin=-max_abs,
                cmax=max_abs,
                showscale=True,
                colorbar=dict(title=color_by),
            ),
            dimensions=dimensions,
        )
    )

    fig.update_layout(title=f"{TITLE} ({len(plot_df):,} lines shown)")
    fig = style_figure(fig, height=500)
    fig.update_layout(margin=dict(l=60, r=60, t=90, b=30))

    st.plotly_chart(fig)
    st.caption(
        "Tip: drag vertically along any axis to filter a range of lines, "
        "or drag axis titles horizontally to reorder axes."
    )
