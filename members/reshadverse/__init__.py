"""Charts by @ReshadVerse.

To add a chart:
1. Copy members/_template/chart_template.py into this folder and rename it.
2. Import it below and add it to the CHARTS list.
"""

from members.reshadverse import chart_heatmap, chart_parallel, chart_sankey

TAB_TITLE = "Flows & Profitability"

CHARTS = [chart_sankey, chart_parallel, chart_heatmap]

