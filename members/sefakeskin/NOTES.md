# Notes - sefakeskin

Use this file to collect material for the report and the presentation.

## My charts

| # | Chart | Type | Question it answers | Interactivity |
|---|-------|------|---------------------|---------------|
| 1 | Profit, sales and orders by country (`chart_world_map.py`) | Choropleth world map (advanced) | Which countries make a profit and which lose money? | Metric dropdown, log/linear color scale switch, hover tooltip, scroll to zoom, drag to pan |
| 2 | Sales and profit of each market over the years (`chart_market_bubbles.py`) | Animated bubble chart (advanced) | How did sales and profit of each market change year by year? | Play button and year slider, log-scale checkbox, hover tooltip, click legend to hide a market |
| 3 | Monthly sales trend and linear regression forecast (`chart_sales_forecast.py`) | Time series + linear regression (ML) | What is the sales trend, and what do the next months look like? | Forecast-length slider (3-12 months), range slider and zoom on the time axis, unified hover |

## Key findings

All numbers are for the full dataset (no sidebar filters).

- **Countries:** the United States (+286k USD), China (+151k) and India (+129k) make the most
  profit. Turkey (-98k), Nigeria (-81k) and the Netherlands (-41k) lose the most.
  29 of the 147 countries make a loss overall.
- **Markets:** every market grew from 2011 to 2014. APAC (1.21M USD sales in 2014) and the EU
  (1.04M) are the biggest. EMEA has the thinnest profit margin (3-8%), Canada the highest
  (about 26%) but very small sales. US sales were flat from 2011 to 2012 while profit still grew.
- **Trend:** monthly sales grow by about 5,900 USD per month. The straight-line model has
  R² ≈ 0.52, so it explains only about half of the variation.
- **Seasonality:** the same pattern repeats every year. February is the weakest month
  (about 136k USD on average), sales jump in June, drop in July and stay high from August to
  December. December (about 395k on average) is almost 3 times February. A straight line
  cannot capture this, so the forecast shows the long-term direction, not exact months.

## Design choices (colors, chart type, why)

- Map: profit uses the shared diverging scale (`RdBu`) centered at 0, so losses are red and
  profits are blue. Sales and orders use the shared sequential scale (`Blues`).
- Map color scale: log by default, linear as an option. The log scale keeps the sign
  (`sign(x) * log10(1 + |x| / 1000)`), so losses stay red. The tooltip always shows the real
  USD values.
- Bubbles: x = sales, y = profit, size = orders, so one chart shows three measures at once.
  The axes are fixed for all years, so the movement of the bubbles shows the real change.
- Forecast: actual sales are a solid line, the trend and forecast a dashed line, and the
  forecast period has a grey background, so past and future are easy to tell apart.
## Problems I faced and how I solved them

- Some country names in the data are old or written differently (e.g. "Myanmar (Burma)",
  "Swaziland", "Macedonia"), so matching by name is not reliable. I mapped every country to
  its ISO-3 code (`country_codes.py`) and draw the map by code.
- On a linear color scale the US (+286k USD) sets the range, but 120 of the 147 countries have a
  profit or loss below 20k. They all looked almost white, e.g. Egypt (+19.7k) and Libya (+2k)
  had nearly the same color. A signed log color scale fixed this: 1k, 10k and 100k are now
  equal steps apart.
- The map first centered on the Pacific (Europe on the left, the Americas on the right).
  Setting the projection rotation to longitude 0 fixed this.
- Without fixed axes, Plotly rescales the axes for every year of the animation, so the bubbles
  would jump. Fixed `range_x` and `range_y` solve this. For the log scale the range must be given as
  powers of ten.
- Sidebar filters can leave months without orders. Monthly sales are built with `resample`,
  so empty months get 0 and the month numbers for the regression stay correct.