"""Charts by @mhakby.

To add a chart:
1. Copy members/_template/chart_template.py into this folder and rename it.
2. Import it below and add it to the CHARTS list.
"""

from members.mhakby import chart_customer_segments, chart_product_network, chart_top_products

TAB_TITLE = "Customers & Products"

CHARTS = [chart_customer_segments, chart_product_network, chart_top_products]
