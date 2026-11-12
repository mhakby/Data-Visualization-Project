"""A1 - Customer segments with K-Means clustering (ML 1).

Each point is one customer. Customers are grouped by K-Means using four numbers:
total sales, total profit, number of orders and average discount.
"""

import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from dashboard.theme import style_figure

TITLE = "Customer segments (K-Means clustering)"
INSIGHT = (
    "With k = 4, the small buyers split into two groups: one gets about 32% average discount "
    "and loses money overall (Cluster 1, about 20% of customers), the other buys with little "
    "discount and stays profitable. The top group (Cluster 4, about 15% of customers) brings "
    "the highest profit per customer."
)

KEY_PREFIX = "mhakby_"

# The numbers K-Means uses to compare customers.
FEATURES = ["total_sales", "total_profit", "orders", "avg_discount"]

# Readable names for axes, tooltips and the summary table.
LABELS = {
    "total_sales": "Total sales (USD)",
    "total_profit": "Total profit (USD)",
    "orders": "Number of orders",
    "avg_discount": "Average discount",
    "customer_name": "Customer",
    "segment": "Segment",
    "cluster": "Cluster",
}


def build_customer_table(df):
    """Turn order rows into one row per customer."""
    customers = df.groupby(["Customer ID", "Customer Name", "Segment"], as_index=False).agg(
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum"),
        orders=("Order ID", "nunique"),
        avg_discount=("Discount", "mean"),
    )
    customers = customers.rename(columns={"Customer Name": "customer_name", "Segment": "segment"})
    return customers


def find_clusters(customers, k):
    """Add a 'cluster' column with K-Means and return the table and the silhouette score."""
    # Sales are in thousands, discount is between 0 and 1. Scaling puts all features
    # on the same scale, otherwise sales would decide the clusters alone.
    scaled = StandardScaler().fit_transform(customers[FEATURES])

    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(scaled)
    score = silhouette_score(scaled, labels)

    customers = customers.copy()
    customers["cluster"] = labels

    # K-Means numbers clusters randomly. We rename them by average sales,
    # so "Cluster 1" always means the customers with the lowest sales.
    order = customers.groupby("cluster")["total_sales"].mean().sort_values().index
    new_names = {old: f"Cluster {number}" for number, old in enumerate(order, start=1)}
    customers["cluster"] = customers["cluster"].map(new_names)

    return customers, score


def render(df):
    k = st.slider(
        "Number of clusters (k)", min_value=2, max_value=6, value=4, key=KEY_PREFIX + "k"
    )

    customers = build_customer_table(df)
    if len(customers) <= k:
        st.info("Not enough customers for this many clusters. Try wider filters or a smaller k.")
        return

    customers, score = find_clusters(customers, k)
    cluster_names = sorted(customers["cluster"].unique())

    fig = px.scatter(
        customers,
        x="total_sales",
        y="total_profit",
        color="cluster",
        size="orders",
        hover_name="customer_name",
        hover_data={"segment": True, "orders": True, "avg_discount": ":.0%", "cluster": False},
        category_orders={"cluster": cluster_names},
        labels=LABELS,
        title=TITLE,
        opacity=0.7,
    )
    # Customers below this line lose money for the store.
    fig.add_hline(y=0, line_dash="dot", line_color="gray", annotation_text="Break-even")
    fig = style_figure(fig, height=500)
    st.plotly_chart(fig)

    # Average values per cluster, to understand what makes each group different.
    summary = customers.groupby("cluster")[FEATURES].mean().round(2)
    summary.insert(0, "customers", customers["cluster"].value_counts())
    summary = summary.rename(columns=LABELS)

    col1, col2 = st.columns([1, 3])
    col1.metric(
        "Silhouette score",
        f"{score:.2f}",
        help="From -1 to 1. Higher means the clusters are better separated.",
    )
    col2.dataframe(summary)
