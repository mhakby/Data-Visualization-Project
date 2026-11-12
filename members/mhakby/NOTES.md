# Notes - mhakby

Use this file to collect material for the report and the presentation.

## My charts

| # | Chart | Type | Question it answers | Interactivity |
|---|-------|------|---------------------|---------------|
| A1 | Customer segments | K-Means clustering scatter (ML) | Which customer groups exist, and how do they differ? | k slider, hover, zoom, legend click, sidebar filters |
| A2 | Sub-categories bought together | Network diagram | Which sub-categories are bought together in the same order? | slider for number of links, hover on nodes and links, zoom, pan, legend click, sidebar filters |
| A3 |       |      |                     |               |

## Key findings

**A1 - Customer segments (all data, k = 4)**

| Cluster | Customers | Avg sales | Avg profit | Avg orders | Avg discount | Meaning |
|---------|-----------|-----------|------------|------------|--------------|---------|
| 1 | 326 (20%) | 1,856 | -235 | 6.6 | 32% | Small buyers with high discounts, they lose money |
| 2 | 485 (31%) | 2,390 | 443 | 6.5 | 7% | Small buyers with low discounts, profitable |
| 3 | 547 (34%) | 11,995 | 1,074 | 25.2 | 14% | Regular customers |
| 4 | 232 (15%) | 18,609 | 3,196 | 28.7 | 12% | Top customers, most profit per customer |

- Discount, not order size, separates profitable small customers from loss-making ones.
- Silhouette score: 0.41 for k = 4 (0.46 for k = 2). k = 4 is a bit lower but gives
  groups that are much easier to explain, so it is the default.

**A2 - Network (all data)**

- 12,235 of 25,035 orders (49%) contain more than one sub-category.
- Strongest pairs: Binders + Storage (944 orders), Art + Binders (895), Art + Storage (833),
  Binders + Paper (684), Binders + Phones (632).
- Binders is the center of the network: it appears in 5,392 orders and is linked to almost
  every other sub-category. Office supplies are the "glue" of most orders.
- All 136 possible pairs of the 17 sub-categories appear at least 38 times, so we only show
  the strongest links.

## Design choices (colors, chart type, why)

**A1**

- Scatter plot of total sales vs total profit: the two numbers a manager cares about most.
- Point size = number of orders, so a third feature is visible without a 3D chart.
- Dotted break-even line at profit = 0 makes the loss-making customers easy to spot.
- Clusters are renamed by average sales (Cluster 1 = lowest), so the numbers stay the same
  when the k slider or the filters change.

**A2**

- Node size = number of orders with that sub-category, line width = number of shared
  orders, node color = category. Strongly connected nodes are pulled closer by the layout
  (`spring_layout` with the pair count as weight).
- Invisible points in the middle of each line make the line value visible on hover.

## Problems I faced and how I solved them

**A1**

- Sales are in thousands and discount is between 0 and 1. Without scaling, K-Means only
  looked at sales. Fixed with `StandardScaler`.
- K-Means gives random cluster numbers, so colors changed every time. Fixed by sorting
  clusters by average sales.

**A2**

- Every sub-category is connected to every other one, so the full network was one big knot.
  Fixed with a slider that shows only the strongest N links.
- Counting pairs takes about 1 second, which made every click slow. Fixed with
  `st.cache_data`, so it is calculated once per filter selection.
