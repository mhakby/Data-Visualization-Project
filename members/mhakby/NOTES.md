# Notes - mhakby

Use this file to collect material for the report and the presentation.

## My charts

| # | Chart | Type | Question it answers | Interactivity |
|---|-------|------|---------------------|---------------|
| A1 | Customer segments | K-Means clustering scatter (ML) | Which customer groups exist, and how do they differ? | k slider, hover, zoom, legend click, sidebar filters |
| A2 |       |      |                     |               |
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

## Design choices (colors, chart type, why)

- Scatter plot of total sales vs total profit: the two numbers a manager cares about most.
- Point size = number of orders, so a third feature is visible without a 3D chart.
- Dotted break-even line at profit = 0 makes the loss-making customers easy to spot.
- Clusters are renamed by average sales (Cluster 1 = lowest), so the numbers stay the same
  when the k slider or the filters change.

## Problems I faced and how I solved them

- Sales are in thousands and discount is between 0 and 1. Without scaling, K-Means only
  looked at sales. Fixed with `StandardScaler`.
- K-Means gives random cluster numbers, so colors changed every time. Fixed by sorting
  clusters by average sales.
