"""A2 - Network of sub-categories that are bought together.

Each node is a sub-category. Two nodes are connected when they appear in the same order.
The thicker the line, the more orders contain both sub-categories.
"""

from itertools import combinations

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.theme import CATEGORY_COLORS, style_figure

TITLE = "Sub-categories bought together (network)"
INSIGHT = (
    "About half of all orders (49%) contain more than one sub-category. Office supplies are "
    "the center of the network: Binders + Storage (944 orders), Art + Binders (895) and "
    "Art + Storage (833) are the most common pairs, and Binders is linked to almost "
    "every other sub-category."
)

KEY_PREFIX = "mhakby_"


@st.cache_data
def count_pairs(df):
    """Count how many orders contain each pair of sub-categories.

    Returns a DataFrame with the columns: source, target, orders.
    """
    # One list of sub-categories per order, e.g. ["Binders", "Paper", "Phones"].
    order_items = df.groupby("Order ID")["Sub-Category"].apply(lambda s: sorted(set(s)))

    pair_counts = {}
    for items in order_items:
        # combinations(["A", "B", "C"], 2) gives ("A", "B"), ("A", "C"), ("B", "C")
        for pair in combinations(items, 2):
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

    rows = [(source, target, count) for (source, target), count in pair_counts.items()]
    pairs = pd.DataFrame(rows, columns=["source", "target", "orders"])
    return pairs.sort_values("orders", ascending=False)


def scale(value, low, high, min_size, max_size):
    """Turn a value between low and high into a size between min_size and max_size."""
    if high == low:
        return (min_size + max_size) / 2
    return min_size + (value - low) / (high - low) * (max_size - min_size)


def render(df):
    pairs = count_pairs(df)
    if pairs.empty:
        st.info("No orders with more than one sub-category for the selected filters.")
        return

    # With very narrow filters there are only a few pairs, then we show all of them.
    if len(pairs) <= 5:
        top_n = len(pairs)
    else:
        top_n = st.slider(
            "Number of strongest links to show",
            min_value=5,
            max_value=min(60, len(pairs)),
            value=min(25, len(pairs)),
            key=KEY_PREFIX + "top_links",
        )
    top_pairs = pairs.head(top_n)

    # Build the graph. The edge weight pulls strongly connected nodes closer together.
    graph = nx.Graph()
    for row in top_pairs.itertuples():
        graph.add_edge(row.source, row.target, weight=row.orders)
    positions = nx.spring_layout(graph, weight="weight", seed=42)

    # Information for each node: its category and in how many orders it appears.
    orders_per_node = df.groupby("Sub-Category")["Order ID"].nunique()
    category_of_node = df.groupby("Sub-Category")["Category"].first()

    fig = go.Figure()

    # 1) Edges: one line per pair, wider line = more shared orders.
    low, high = top_pairs["orders"].min(), top_pairs["orders"].max()
    for row in top_pairs.itertuples():
        x0, y0 = positions[row.source]
        x1, y1 = positions[row.target]
        fig.add_trace(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(width=scale(row.orders, low, high, 1, 8), color="lightgray"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # 2) Invisible points in the middle of each edge, so hovering a line shows its value.
    middle_x, middle_y, edge_text = [], [], []
    for row in top_pairs.itertuples():
        (x0, y0), (x1, y1) = positions[row.source], positions[row.target]
        middle_x.append((x0 + x1) / 2)
        middle_y.append((y0 + y1) / 2)
        edge_text.append(f"{row.source} + {row.target}<br>{row.orders:,} orders")
    fig.add_trace(
        go.Scatter(
            x=middle_x,
            y=middle_y,
            mode="markers",
            marker=dict(size=10, opacity=0),
            text=edge_text,
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # 3) Nodes: one trace per category, so the legend shows the categories.
    node_low, node_high = orders_per_node.min(), orders_per_node.max()
    categories = sorted(category_of_node[list(graph.nodes)].unique())
    for color, category in zip(CATEGORY_COLORS, categories):
        nodes = [node for node in graph.nodes if category_of_node[node] == category]
        fig.add_trace(
            go.Scatter(
                x=[positions[node][0] for node in nodes],
                y=[positions[node][1] for node in nodes],
                mode="markers+text",
                name=category,
                text=nodes,
                textposition="top center",
                customdata=[orders_per_node[node] for node in nodes],
                marker=dict(
                    size=[scale(orders_per_node[n], node_low, node_high, 14, 40) for n in nodes],
                    color=color,
                    line=dict(width=1, color="white"),
                ),
                hovertemplate="<b>%{text}</b><br>In %{customdata:,} orders<extra></extra>",
            )
        )

    fig.update_layout(
        title=TITLE,
        legend_title_text="Category",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    fig = style_figure(fig, height=550)
    st.plotly_chart(fig)

    with st.expander("Top 10 pairs"):
        table = pairs.head(10).rename(
            columns={"source": "Sub-category 1", "target": "Sub-category 2", "orders": "Orders"}
        )
        st.dataframe(table, hide_index=True)
