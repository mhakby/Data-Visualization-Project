"""Sankey diagram (B1): multi-stage sales and quantity flow across store dimensions."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.theme import CATEGORY_COLORS, style_figure

TITLE = "Sales Flow Across Segments, Markets, and Product Hierarchy"
INSIGHT = (
    "The Consumer segment generates roughly 51% of total revenue across all markets, "
    "with Technology and Furniture driving the largest dollar flows while Office Supplies "
    "accounts for the highest volume of individual items sold."
)

KEY_PREFIX = "reshadverse_sankey_"

FLOW_PATHS = {
    "Segment -> Category -> Sub-Category": ["Segment", "Category", "Sub-Category"],
    "Market -> Segment -> Category": ["Market", "Segment", "Category"],
    "Market -> Category -> Sub-Category": ["Market", "Category", "Sub-Category"],
}


def _to_rgba(color: str, alpha: float = 0.35) -> str:
    """Convert an 'rgb(r, g, b)' string from Plotly palettes into 'rgba(r, g, b, alpha)'."""
    if color.startswith("rgb(") and color.endswith(")"):
        return color.replace("rgb(", "rgba(").rstrip(")") + f", {alpha})"
    return color


def _build_sankey_links(df: pd.DataFrame, columns: list[str], metric: str):
    """Build node labels and (source, target, value) link lists across adjacent columns."""
    labels = []
    for col in columns:
        for val in sorted(df[col].dropna().unique()):
            if val not in labels:
                labels.append(val)

    node_map = {label: idx for idx, label in enumerate(labels)}

    sources, targets, values = [], [], []
    for src_col, tgt_col in zip(columns[:-1], columns[1:]):
        grouped = df.groupby([src_col, tgt_col], as_index=False)[metric].sum()
        grouped = grouped[grouped[metric] > 0]
        for _, row in grouped.iterrows():
            sources.append(node_map[row[src_col]])
            targets.append(node_map[row[tgt_col]])
            values.append(float(row[metric]))

    return labels, sources, targets, values


def render(df: pd.DataFrame):
    """Render the interactive Sankey diagram for the filtered dataset."""
    if df.empty:
        st.info("No data available for the selected filters.")
        return

    col1, col2 = st.columns(2)
    with col1:
        path_label = st.selectbox(
            "Flow hierarchy",
            options=list(FLOW_PATHS.keys()),
            key=KEY_PREFIX + "path",
        )
    with col2:
        metric = st.selectbox(
            "Flow size metric",
            options=["Sales", "Quantity"],
            key=KEY_PREFIX + "metric",
        )

    columns = FLOW_PATHS[path_label]
    labels, sources, targets, values = _build_sankey_links(df, columns, metric)

    node_colors = [CATEGORY_COLORS[i % len(CATEGORY_COLORS)] for i in range(len(labels))]
    link_colors = [_to_rgba(node_colors[src], 0.35) for src in sources]

    value_prefix = "$" if metric == "Sales" else ""
    value_suffix = " items" if metric == "Quantity" else ""

    node_hover = (
        "<b>%{label}</b><br>Total "
        + metric
        + ": "
        + value_prefix
        + "%{value:,.0f}"
        + value_suffix
        + "<extra></extra>"
    )
    link_hover = (
        "<b>%{source.label} -> %{target.label}</b><br>"
        + metric
        + ": "
        + value_prefix
        + "%{value:,.0f}"
        + value_suffix
        + "<extra></extra>"
    )

    fig = go.Figure(
        data=[
            go.Sankey(
                valueformat=",.0f",
                valuesuffix=value_suffix,
                node=dict(
                    pad=16,
                    thickness=20,
                    line=dict(color="white", width=1),
                    label=labels,
                    color=node_colors,
                    hovertemplate=node_hover,
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                    hovertemplate=link_hover,
                ),
            )
        ]
    )

    fig.update_layout(
        title=f"{TITLE} ({metric}: {path_label})",
        font=dict(size=12),
    )
    fig = style_figure(fig, height=520)

    st.plotly_chart(fig)
