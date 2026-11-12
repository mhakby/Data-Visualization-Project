# Notes - ReshadVerse

Use this file to collect material for the report and the presentation.

## My charts

| # | Chart | Type | Question it answers | Interactivity |
|---|-------|------|---------------------|---------------|
| 1 | Sales Flow (`chart_sankey.py`) | Sankey diagram (advanced) | Where do sales and item quantities come from, and which categories do they go into? | Dropdown to change the flow path, dropdown to switch between Sales ($) and Quantity, drag nodes with the mouse, hover tooltips |
| 2 | Discount, Quantity, Shipping and Profit (`chart_parallel.py`) | Parallel coordinates (advanced) | How do discounts and shipping costs affect profit? | Dropdown for view mode (averages vs single orders), dropdown for line color, slider for sample size, drag on axes to filter lines |
| 3 | Profit by Sub-Category and Market (`chart_heatmap.py`) | Heatmap | Which products make or lose money in each market? | Dropdown for metric (Profit, Profit Margin, Sales), dropdown for Market vs Region, checkbox to show/hide numbers, hover tooltips |

## Key findings

All numbers are for the full dataset (no sidebar filters).

### 1. Sankey Diagram (Sales Flow)
- **Biggest customer group:** Everyday buyers (**Consumer**) bring in **more than half of all sales** (51.5%, or $6.51M). Companies (**Corporate**) bring 30.3%, and **Home Office** brings 18.2%.
- **Sales in dollars ($):** **Technology** brings the most money ($4.74M), followed by **Furniture** ($4.11M) and **Office Supplies** ($3.79M).
- **Sales by item count (Quantity):** When we switch from dollars to number of items, **Office Supplies** becomes #1 by far (**60.6%** of all items sold). People buy lots of cheap items like binders and paper, while Technology items are bought less often but cost much more.

### 2. Parallel Coordinates (Discounts & Profit)
- **No discount = good profit:** Orders with **0% discount** make a strong profit (about **+26.5%** margin on average).
- **Small discount (1% to 20%) = still okay:** These orders still make money (about **+15.6%** margin).
- **Big discount (over 20%) = guaranteed loss:** Almost every order with a discount above **20%** loses money (red lines). The average margin drops to **-40.8%**, causing over **-$940k** in total losses.
- **Main takeaway:** Huge discounts—not shipping costs or order quantities—are the main reason the store loses money.

### 3. Heatmap (Sub-Categories x Markets)
- **Worst product:** **Tables** is the biggest money-loser in the whole store (**-$64k** total loss). It loses money in 5 out of 7 markets, especially in **APAC** (-$26.6k), **EU** (-$18.9k), and **US** (-$17.7k).
- **Best products:** **Copiers** (+$259k), **Phones** (+$217k), and **Bookcases** (+$162k) make the highest profit.
- **Best and weakest markets:** **APAC** (+$436k) and **EU** (+$372k) make the most profit overall, while **EMEA** has very low profit margins across many products.

## Design choices (colors, chart type, why)

- **Chart 1 (Sankey):** I used a Sankey chart because it shows step-by-step how money moves from customer groups to product categories. Each ribbon uses the same color as its starting block (with light transparency) so it is easy to follow with your eyes.
- **Chart 2 (Parallel Coordinates):** I used this chart to compare 6 numbers at the same time on vertical axes. I used the red-to-blue (`RdBu`) color scale: **blue = profit**, **red = loss**, and **white = zero**.
- **Chart 3 (Heatmap):** I sorted the rows and columns automatically so the most profitable products are at the top and the worst ones (like Tables) are at the bottom. I used `RdBu` for Profit/Margin (so losses are clearly red) and simple `Blues` for Sales (since sales are never negative).

## Problems I faced and how I solved them

- **Problem 1 — Too many lines on Parallel Coordinates:**
  - *What happened:* The dataset has 51,290 rows. Drawing 51,290 lines at once made the chart look like a solid block of color and made the browser slow.
  - *How I fixed it:* By default, I grouped the data into 51 clean average lines (`Segment x Sub-Category`). I also added a second mode with a slider (200 to 3,000 rows) if the user wants to look at individual orders.
- **Problem 2 — Wrong colors for losses in Parallel Coordinates:**
  - *What happened:* Because negative losses go much lower than positive profits, the middle of the color scale (white) was below zero, so some losing orders looked blue.
  - *How I fixed it:* I set the minimum and maximum of the color bar to be equal on both sides of zero (`-max` to `+max`), so `0` is always right in the middle (white).
- **Problem 3 — Fair Profit Margin calculation in the Heatmap:**
  - *What happened:* Taking a simple average of the `Profit Margin` column gave a tiny $5 order the same importance as a big $5,000 order.
  - *How I fixed it:* For each box in the heatmap, I calculated `Total Profit / Total Sales * 100`, which gives the true profit margin for that market and product.