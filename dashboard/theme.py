"""Shared look for all charts, so the dashboard feels consistent.

Use these colors in your charts instead of picking your own.
"""

import plotly.express as px
import plotly.io as pio

# Color-blind friendly palette for categories.
CATEGORY_COLORS = px.colors.qualitative.Safe

# For values that go from low to high (e.g. sales amount).
SEQUENTIAL_SCALE = "Blues"

# For values that can be negative or positive (e.g. profit / loss).
DIVERGING_SCALE = "RdBu"

CHART_HEIGHT = 450


def apply_theme():
    """Set default Plotly settings. Called once at the top of app.py."""
    pio.templates.default = "plotly_white"
    px.defaults.template = "plotly_white"
    px.defaults.color_discrete_sequence = CATEGORY_COLORS
    px.defaults.color_continuous_scale = SEQUENTIAL_SCALE


def style_figure(fig, height=CHART_HEIGHT):
    """Give a Plotly figure the same size, margins and legend position as the others."""
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        title_x=0.0,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
