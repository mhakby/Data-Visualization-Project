"""A3 - Products with the highest profit and the biggest losses.

One bar per product. The user chooses top or bottom products, how many to show,
and whether the bars are colored by category or by average discount.
"""

import plotly.express as px
import streamlit as st

from dashboard.theme import SEQUENTIAL_SCALE, style_figure

TITLE = "Most profitable products and biggest losses"
INSIGHT = (
    "678 of 3,788 products (18%) lose money in total, about 248,000 USD together. "
    "The 10 biggest losers (mostly tables and printers) get 37% average discount, while the "
    "10 most profitable products (mostly smart phones) get only 12%."
)

KEY_PREFIX = "mhakby_"

MAX_NAME_LENGTH = 40

LABELS = {
    "profit": "Total profit (USD)",
    "sales": "Total sales (USD)",
    "avg_discount": "Average discount",
    "category": "Category",
    "sub_category": "Sub-category",
    "product": "Product",
}


def build_product_table(df):
    """One row per product with its total profit, total sales and average discount."""
    products = df.groupby("Product Name", as_index=False).agg(
        category=("Category", "first"),
        sub_category=("Sub-Category", "first"),
        profit=("Profit", "sum"),
        sales=("Sales", "sum"),
        avg_discount=("Discount", "mean"),
    )
    return products.rename(columns={"Product Name": "product"})


def shorten(name):
    """Cut long product names so they fit next to the bars, e.g. 'Cubify CubeX 3D Pri...'."""
    if len(name) <= MAX_NAME_LENGTH:
        return name
    return name[: MAX_NAME_LENGTH - 3] + "..."


def render(df):
    products = build_product_table(df)

    # Small numbers above the chart, they change with the sidebar filters.
    losing = products[products["profit"] < 0]
    col1, col2 = st.columns(2)
    col1.metric(
        "Products that lose money",
        f"{len(losing):,} of {len(products):,}",
        help="Products whose total profit is below zero.",
    )
    col2.metric("Total loss of these products", f"{losing['profit'].sum():,.0f} USD")

    col1, col2, col3 = st.columns(3)
    show = col1.radio(
        "Show", ["Most profitable", "Biggest losses"], horizontal=True, key=KEY_PREFIX + "show"
    )
    count = col2.slider(
        "Number of products", min_value=5, max_value=20, value=10, key=KEY_PREFIX + "count"
    )
    color_by = col3.selectbox(
        "Color bars by", ["Category", "Average discount"], key=KEY_PREFIX + "color_by"
    )

    if show == "Most profitable":
        selected = products.nlargest(count, "profit")
        chart_title = f"Top {count} most profitable products"
    else:
        selected = products.nsmallest(count, "profit")
        chart_title = f"Top {count} products with the biggest losses"

    color_settings = {}
    if color_by == "Category":
        color_settings["color"] = "category"
        # Same category order as the network chart, so the colors match.
        color_settings["category_orders"] = {"category": sorted(products["category"].unique())}
    else:
        color_settings["color"] = "avg_discount"
        color_settings["color_continuous_scale"] = SEQUENTIAL_SCALE
        color_settings["range_color"] = (0, 0.7)

    fig = px.bar(
        selected,
        x="profit",
        y="product",
        orientation="h",
        text_auto=".3s",
        hover_data={"sub_category": True, "sales": ":,.0f", "avg_discount": ":.0%"},
        labels=LABELS,
        title=chart_title,
        **color_settings,
    )

    # The y axis uses the full names (so two products never share one bar),
    # but shows the shortened names as labels.
    fig.update_yaxes(
        tickvals=selected["product"],
        ticktext=[shorten(name) for name in selected["product"]],
        title=None,
    )
    # Biggest bar on top: for profits the largest value, for losses the most negative one.
    if show == "Most profitable":
        fig.update_yaxes(categoryorder="total ascending")
    else:
        fig.update_yaxes(categoryorder="total descending")

    fig = style_figure(fig, height=200 + count * 28)
    st.plotly_chart(fig)
