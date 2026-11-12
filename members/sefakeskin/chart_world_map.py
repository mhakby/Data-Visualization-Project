"""C1 - Profit by country: choropleth world map (issue #10)."""

import numpy as np
import plotly.express as px
import streamlit as st

from dashboard.theme import DIVERGING_SCALE, SEQUENTIAL_SCALE, style_figure
from members.sefakeskin.country_codes import COUNTRY_TO_ISO3

TITLE = "Profit, sales and orders by country"
INSIGHT = (
    "The United States, China and India make the most profit, while Turkey, Nigeria and the "
    "Netherlands lose the most money; 29 of the 147 countries make a loss overall."
)

KEY_PREFIX = "sefakeskin_"

# Label shown in the dropdown -> (column in the grouped table, unit for the log scale).
# The unit is the value where the log scale starts to grow quickly: 1,000 USD for money,
# 10 orders for the number of orders.
METRICS = {
    "Profit (USD)": ("Profit", 1_000),
    "Sales (USD)": ("Sales", 1_000),
    "Number of orders": ("Orders", 10),
}

LOG_SCALE = "Log (shows small differences)"
LINEAR_SCALE = "Linear"


def country_summary(df):
    """One row per country with total profit, total sales and the number of orders."""
    summary = (
        df.groupby("Country")
        .agg(Profit=("Profit", "sum"), Sales=("Sales", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
    )
    summary["ISO3"] = summary["Country"].map(COUNTRY_TO_ISO3)
    return summary


def signed_log(values, unit):
    """Log scale that keeps the sign: 0 stays 0, losses stay negative.

    Most countries have a profit between -20k and +20k USD, while the US has +286k. On a linear
    color scale all the small countries get almost the same color. On this scale 1k, 10k and
    100k are equal steps apart, so small differences become visible too.
    """
    return np.sign(values) * np.log10(1 + np.abs(values) / unit)


def log_colorbar_ticks(values, unit):
    """Tick positions (on the log scale) and labels (in real units) for the color bar."""
    ticks = [0]
    step = unit
    while step <= np.abs(values).max():
        if values.max() >= step:
            ticks.append(step)
        if values.min() <= -step:
            ticks.insert(0, -step)
        step *= 10
    labels = [f"{tick / 1000:,.0f}k" if abs(tick) >= 1000 else f"{tick:,}" for tick in ticks]
    return signed_log(np.array(ticks), unit).tolist(), labels


def render(df):
    col_metric, col_scale = st.columns(2)
    metric_label = col_metric.selectbox("Metric", list(METRICS), key=KEY_PREFIX + "map_metric")
    scale = col_scale.radio(
        "Color scale",
        [LOG_SCALE, LINEAR_SCALE],
        horizontal=True,
        key=KEY_PREFIX + "map_scale",
    )
    metric, unit = METRICS[metric_label]

    all_countries = country_summary(df)
    missing = all_countries.loc[all_countries["ISO3"].isna(), "Country"].tolist()
    summary = all_countries.dropna(subset=["ISO3"]).copy()
    if scale == LOG_SCALE:
        summary["Color"] = signed_log(summary[metric], unit)
    else:
        summary["Color"] = summary[metric]

    # Profit can be negative, so it gets a diverging scale with white at 0 (red = loss).
    if metric == "Profit":
        color_options = dict(color_continuous_scale=DIVERGING_SCALE, color_continuous_midpoint=0)
    else:
        color_options = dict(color_continuous_scale=SEQUENTIAL_SCALE)

    fig = px.choropleth(
        summary,
        locations="ISO3",
        locationmode="ISO-3",
        color="Color",
        hover_name="Country",
        # The tooltip always shows the real values, also on the log scale.
        hover_data={
            "ISO3": False,
            "Color": False,
            "Profit": ":,.0f",
            "Sales": ":,.0f",
            "Orders": ":,",
        },
        title=f"{metric_label} by country",
        **color_options,
    )
    # Keep Europe/Africa in the middle (longitude 0); without this the map can center on the
    # Pacific, which splits the Americas and Asia to opposite sides.
    fig.update_geos(
        projection_type="natural earth",
        projection_rotation_lon=0,
        center_lon=0,
        showcountries=True,
        countrycolor="#bbbbbb",
    )

    colorbar = dict(title=metric_label)
    if scale == LOG_SCALE:
        tick_values, tick_labels = log_colorbar_ticks(summary[metric], unit)
        colorbar.update(title=f"{metric_label}<br>(log scale)", tickvals=tick_values,
                        ticktext=tick_labels)
    fig.update_layout(coloraxis_colorbar=colorbar)
    fig = style_figure(fig, height=520)

    # Scroll to zoom and drag to pan on the map.
    st.plotly_chart(fig, config={"scrollZoom": True})

    if missing:
        st.caption("Countries without a map code (not shown): " + ", ".join(missing))
