"""C3 - Sales trend and forecast: time series with linear regression (issue #12)."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression

from dashboard.theme import CATEGORY_COLORS, style_figure

TITLE = "Monthly sales trend and linear regression forecast"
INSIGHT = (
    "Monthly sales grow by about 5,900 USD per month, but the straight line explains only about "
    "half of the variation (R² ≈ 0.52): it misses the seasonal peaks in June and from August "
    "to December."
)

KEY_PREFIX = "sefakeskin_"


def monthly_sales(df):
    """Total sales per month. Months without orders get 0, so the month numbers stay correct."""
    sales = df.set_index("Order Date")["Sales"].resample("MS").sum()
    return sales.reset_index().rename(columns={"Order Date": "Month"})


def fit_trend(monthly, months_ahead):
    """Fit sales = a + b * month_number and predict the next `months_ahead` months.

    Returns the model, the R² score on the past months and a table with the trend line for the
    past months plus the forecast for the future months.
    """
    month_numbers = pd.DataFrame({"month_number": range(len(monthly))})
    model = LinearRegression().fit(month_numbers, monthly["Sales"])
    r2 = model.score(month_numbers, monthly["Sales"])

    all_numbers = pd.DataFrame({"month_number": range(len(monthly) + months_ahead)})
    all_months = pd.date_range(monthly["Month"].iloc[0], periods=len(all_numbers), freq="MS")
    trend = pd.DataFrame({"Month": all_months, "Trend": model.predict(all_numbers)})
    return model, r2, trend


def render(df):
    monthly = monthly_sales(df)
    if len(monthly) < 3:
        st.info("Select at least 3 months in the sidebar to fit a trend.")
        return

    months_ahead = st.slider(
        "Months to forecast",
        min_value=3,
        max_value=12,
        value=6,
        key=KEY_PREFIX + "forecast_months",
    )
    model, r2, trend = fit_trend(monthly, months_ahead)
    last_month = monthly["Month"].iloc[-1]

    col_r2, col_slope = st.columns(2)
    col_r2.metric("R² of the linear trend", f"{r2:.2f}")
    col_slope.metric("Trend: change in sales per month", f"{model.coef_[0]:+,.0f} USD")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly["Month"],
            y=monthly["Sales"],
            name="Actual sales",
            mode="lines+markers",
            line=dict(color=CATEGORY_COLORS[0]),
            hovertemplate="%{x|%b %Y}<br>Sales: %{y:,.0f} USD<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=trend["Month"],
            y=trend["Trend"],
            name="Linear trend + forecast",
            mode="lines",
            line=dict(color=CATEGORY_COLORS[1], dash="dash"),
            hovertemplate="%{x|%b %Y}<br>Trend: %{y:,.0f} USD<extra></extra>",
        )
    )
    # Light background on the forecast part, so past and future are easy to tell apart.
    fig.add_vrect(
        x0=last_month,
        x1=trend["Month"].iloc[-1],
        fillcolor="#999999",
        opacity=0.12,
        line_width=0,
        annotation_text="Forecast",
        annotation_position="top left",
    )
    fig.update_layout(
        title=TITLE,
        xaxis_title="Month",
        yaxis_title="Sales (USD)",
        legend_title_text="Series",
        hovermode="x unified",
    )
    # Range slider under the chart to pick a time window; drag on the chart to zoom.
    fig.update_xaxes(rangeslider_visible=True)
    fig = style_figure(fig, height=520)

    st.plotly_chart(fig)
