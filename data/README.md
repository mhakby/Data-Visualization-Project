# Data

## Source

**Global Superstore** - retail orders of a global online store, 2011-2014.
Downloaded from [Kaggle](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset).

| File | Description |
|------|-------------|
| `raw/Global_Superstore2.csv` | Original file, not edited (latin-1 encoding) |
| `processed/superstore_clean.csv` | Cleaned file used by the app (UTF-8). Created by `python -m scripts.preprocess` |

## Cleaning steps

Done in `dashboard/preprocessing.py`:

| Step | What we found | What we did |
|------|---------------|-------------|
| Encoding | The file is not UTF-8 | Read it as latin-1, save the clean file as UTF-8 |
| Extra spaces | 16 text values had spaces at the start or end | Removed the spaces |
| Duplicates | 0 duplicate rows | Nothing to remove (the check stays in the code) |
| Missing values | `Postal Code` is 80.5% empty (only US orders have one) | Dropped the column |
| Unused column | `Row ID` is only a row number | Dropped the column |
| Dates | Stored as text, day-month-year | Converted to datetime |
| Invalid rows | Checked for "shipped before ordered" and sales <= 0 | 0 rows found (the check stays in the code) |
| Outliers | 1.5 * IQR rule: Sales 11.0%, Profit 19.0%, Shipping Cost 11.5% | **Kept**, because large orders and big losses are real sales. The sidebar checkbox can hide Sales outliers. |

Result: **51,290 rows, 26 columns**.

## Columns (cleaned file)

| Column | Type | Description |
|--------|------|-------------|
| Order ID | text | Order number. One order can have several rows (products) |
| Order Date | date | Date of the order (2011-01-01 to 2014-12-31) |
| Ship Date | date | Date the order was shipped |
| Ship Mode | category | Same Day, First Class, Second Class, Standard Class |
| Customer ID | text | Customer number (1,590 customers) |
| Customer Name | text | Customer name |
| Segment | category | Consumer, Corporate, Home Office |
| City | text | City of the customer |
| State | text | State / province |
| Country | text | Country (147 countries) |
| Market | category | APAC, LATAM, EU, US, EMEA, Africa, Canada |
| Region | category | 13 regions, e.g. Central, South, Oceania |
| Product ID | text | Product number |
| Category | category | Furniture, Office Supplies, Technology |
| Sub-Category | category | 17 sub-categories, e.g. Phones, Chairs, Binders |
| Product Name | text | Product name (3,788 products) |
| Sales | number | Sales amount in USD |
| Quantity | number | Number of items |
| Discount | number | Discount rate, 0 to 0.85 |
| Profit | number | Profit in USD (negative = loss) |
| Shipping Cost | number | Shipping cost in USD |
| Order Priority | category | Low, Medium, High, Critical |
| **Year** | number | *New:* year of Order Date |
| **Month** | number | *New:* month of Order Date (1-12) |
| **Shipping Days** | number | *New:* days between Order Date and Ship Date (0-7) |
| **Profit Margin** | number | *New:* Profit / Sales (e.g. 0.25 = 25%) |
