"""Charts by @sefakeskin.

To add a chart:
1. Copy members/_template/chart_template.py into this folder and rename it.
2. Import it below and add it to the CHARTS list.
"""

from members.sefakeskin import chart_market_bubbles, chart_sales_forecast, chart_world_map

TAB_TITLE = "Geography & Time"

CHARTS = [chart_world_map, chart_market_bubbles, chart_sales_forecast]
