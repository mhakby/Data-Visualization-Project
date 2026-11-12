# Notes - mhakby

Use this file to collect material for the report and the presentation.

## My charts

| # | Chart | Type | Question it answers | Interactivity |
|---|-------|------|---------------------|---------------|
| A1 |       |      |                     |               |
| A2 | Sub-categories bought together | Network diagram | Which sub-categories are bought together in the same order? | slider for number of links, hover on nodes and links, zoom, pan, legend click, sidebar filters |
| A3 |       |      |                     |               |

## Key findings

**A2 - Network (all data)**

- 12,235 of 25,035 orders (49%) contain more than one sub-category.
- Strongest pairs: Binders + Storage (944 orders), Art + Binders (895), Art + Storage (833),
  Binders + Paper (684), Binders + Phones (632).
- Binders is the center of the network: it appears in 5,392 orders and is linked to almost
  every other sub-category. Office supplies are the "glue" of most orders.
- All 136 possible pairs of the 17 sub-categories appear at least 38 times, so we only show
  the strongest links.

## Design choices (colors, chart type, why)

- Network: node size = number of orders with that sub-category, line width = number of shared
  orders, node color = category. Strongly connected nodes are pulled closer by the layout
  (`spring_layout` with the pair count as weight).
- Invisible points in the middle of each line make the line value visible on hover.

## Problems I faced and how I solved them

- Every sub-category is connected to every other one, so the full network was one big knot.
  Fixed with a slider that shows only the strongest N links.
- Counting pairs takes about 1 second, which made every click slow. Fixed with
  `st.cache_data`, so it is calculated once per filter selection.
