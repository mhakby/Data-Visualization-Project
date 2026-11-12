"""C2 - Markets over the years: animated bubble chart (issue #11)."""

import math

import plotly.express as px
import streamlit as st

from dashboard.theme import CATEGORY_COLORS, style_figure

TITLE = "Sales and profit of each market over the years"
INSIGHT = (
    "Every market grew from 2011 to 2014; APAC and the EU lead in both sales and profit, "
    "while EMEA sells a lot but keeps the thinnest profit margin (under 8%)."
)

KEY_PREFIX = "sefakeskin_"

# Animation speed in milliseconds (Plotly's default is 500 for both).
FRAME_MS = 1500
TRANSITION_MS = 1200


def market_year_summary(df):
    """One row per market and year with total sales, total profit and the number of orders."""
    return (
        df.groupby(["Market", "Year"])
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values(["Year", "Market"])
    )


def padded_range(values, padding=0.1):
    """Axis range from the smallest to the largest value, with some space on both sides."""
    low, high = values.min(), values.max()
    space = (high - low) * padding or abs(high) * padding or 1
    return [low - space, high + space]


def slow_down_animation(fig, frame_ms=FRAME_MS, transition_ms=TRANSITION_MS):
    """Make the play button slower and smoother than Plotly's default (0.5 s per year).

    frame_ms is how long each year stays on screen, transition_ms how long the bubbles take
    to move to the next year. A smooth easing makes the bubbles grow gradually.
    """
    if not fig.layout.updatemenus:  # no animation, e.g. when only one year is selected
        return
    play_button = fig.layout.updatemenus[0].buttons[0]
    play_button.args[1]["frame"]["duration"] = frame_ms
    play_button.args[1]["transition"]["duration"] = transition_ms
    play_button.args[1]["transition"]["easing"] = "cubic-in-out"
    # The same speed when the user drags the year slider.
    for step in fig.layout.sliders[0].steps:
        step.args[1]["transition"]["duration"] = transition_ms


def render(df):
    log_x = st.checkbox(
        "Log scale for sales (makes small markets like Canada easier to see)",
        key=KEY_PREFIX + "bubbles_log_x",
    )

    summary = market_year_summary(df)
    summary["Profit Margin"] = summary["Profit"] / summary["Sales"]

    # Fixed axis ranges, otherwise the axes jump between the years of the animation.
    # For a log axis Plotly expects the range as powers of ten.
    if log_x:
        log_sales = summary["Sales"].map(math.log10)
        range_x = [log_sales.min() - 0.2, log_sales.max() + 0.2]
    else:
        range_x = [0, padded_range(summary["Sales"])[1]]
    range_y = padded_range(summary["Profit"])

    fig = px.scatter(
        summary,
        x="Sales",
        y="Profit",
        size="Orders",
        color="Market",
        hover_name="Market",
        hover_data={
            "Year": True,
            "Sales": ":,.0f",
            "Profit": ":,.0f",
            "Orders": ":,",
            "Profit Margin": ":.1%",
            "Market": False,
        },
        animation_frame="Year",
        animation_group="Market",
        color_discrete_sequence=CATEGORY_COLORS,
        size_max=60,
        log_x=log_x,
        range_x=range_x,
        range_y=range_y,
        title=TITLE,
    )
    fig.update_layout(
        xaxis_title="Total sales (USD)",
        yaxis_title="Total profit (USD)",
        legend_title_text="Market (click to hide)",
    )
    slow_down_animation(fig)
    fig = style_figure(fig, height=560)

    # style_figure puts the legend above the chart; the play button and year slider stay below.
    st.plotly_chart(fig)
    st.caption("Bubble size = number of orders. Press play or drag the year slider.")
