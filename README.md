# Exploratory Data Visualization Dashboard

An interactive dashboard built with **Python** and **Streamlit** to explore a real-world dataset
through 9 interactive visualizations and 2 machine learning models.

CEN445 Introduction to Data Visualization - Team Project (2026-2027)

**Team:** Mehmet Hadi Akbey, Reshad Aliyev, Sefa Keskin

**One-page report:** [reports/CEN445_Team_Report.pdf](reports/CEN445_Team_Report.pdf)

## Dataset

| | |
|---|---|
| **Name** | Global Superstore |
| **Source** | [Kaggle - Global Super Store Dataset](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset) |
| **Size** | 51,290 rows, 24 columns (raw) -> 26 columns after cleaning |
| **Description** | Orders of a global online store from 2011 to 2014: dates, customers, countries, markets, product categories, sales, discount, profit and shipping cost |

The raw file is stored in `data/raw/` and the cleaned file in `data/processed/`.
See [data/README.md](data/README.md) for the cleaning steps and the list of columns.

## Project Structure

```
├── app.py                  # Main Streamlit app (creates the tabs and the sidebar)
├── dashboard/              # Shared code used by everyone
│   ├── config.py           # File paths, column names, app texts
│   ├── data_loader.py      # Loads the cleaned dataset (cached)
│   ├── preprocessing.py    # Cleaning helpers: missing values, outliers, ...
│   ├── filters.py          # Sidebar filters shared by all charts
│   ├── overview.py         # "Overview" tab
│   └── theme.py            # Shared colors and chart style
├── members/                # One folder per team member
│   ├── _template/          # Copy files from here to start a new chart
│   ├── mhakby/
│   ├── reshadverse/
│   └── sefakeskin/
├── scripts/preprocess.py   # Turns data/raw into data/processed
├── data/                   # raw/ and processed/ data files
├── notebooks/              # Optional exploration notebooks
├── reports/                # One-page project report
└── tests/                  # Automated checks (run by GitHub Actions)
```

## Setup

Requirements: Python 3.11+ and Git.

```bash
# 1. Clone the repository
git clone https://github.com/mhakby/Data-Visualization-Project.git
cd Data-Visualization-Project

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 3. Install the packages
pip install -r requirements-dev.txt

# 4. Create the cleaned dataset
python -m scripts.preprocess

# 5. Start the dashboard
streamlit run app.py
```

Run the checks before opening a pull request:

```bash
ruff check .
pytest
```

## Visualizations

The dashboard has an **Overview** tab (dataset size, preview, column summary) and one tab per
member with three charts each. All charts react to the sidebar filters (market, category,
segment, date range, hide Sales outliers). Insights below are for the full dataset.

| # | Chart | Type | Insight | Author |
|---|-------|------|---------|--------|
| A1 | Customer segments | K-Means clustering (advanced, **ML**) | With k = 4, about 20% of customers get ~32% average discount and lose money overall, while the top 15% bring the highest profit per customer. | Mehmet Hadi Akbey |
| A2 | Sub-categories bought together | Network diagram (advanced) | 49% of orders contain more than one sub-category; Binders + Storage (944 orders) is the most common pair and Binders links to almost everything. | Mehmet Hadi Akbey |
| A3 | Most profitable products and biggest losses | Bar chart | 678 of 3,788 products (18%) lose about 248k USD in total; the 10 biggest losers get 37% average discount vs. 12% for the 10 most profitable. | Mehmet Hadi Akbey |
| B1 | Sales flow | Sankey diagram (advanced) | Consumers bring 51.5% of sales; Technology earns the most money, but Office Supplies is 60.6% of all items sold. | Reshad Aliyev |
| B2 | Discount, quantity, shipping cost and profit | Parallel coordinates (advanced) | Orders with more than 20% discount almost always lose money (average margin -40.8%), regardless of quantity or shipping cost. | Reshad Aliyev |
| B3 | Profit by sub-category and market | Heatmap | Tables lose money in 5 of 7 markets (-64k USD in total), while Copiers, Phones and Bookcases make the highest profit. | Reshad Aliyev |
| C1 | Profit by country | Choropleth map (advanced) | The US, China and India make the most profit; Turkey, Nigeria and the Netherlands lose the most; 29 of 147 countries make a loss. | Sefa Keskin |
| C2 | Markets over the years | Animated bubble chart (advanced) | Every market grew from 2011 to 2014; APAC and the EU lead, while EMEA has the thinnest profit margin (under 8%). | Sefa Keskin |
| C3 | Sales trend and forecast | Time series + linear regression (**ML**) | Sales grow by about 5,900 USD per month, but the straight line (R² ≈ 0.52) misses the strong yearly seasonality (December ≈ 3 × February). | Sefa Keskin |

**Main finding across charts:** high discounts are the main reason for losses. The same pattern
appears for customers (A1), products (A3, B3) and single orders (B2).

## Team and Contributions

| Member | GitHub | Contributions |
|--------|--------|---------------|
| Mehmet Hadi Akbey | [@mhakby](https://github.com/mhakby) | Shared work (see below); charts A1 (K-Means customer segments), A2 (network), A3 (top / bottom products) |
| Reshad Aliyev | [@ReshadVerse](https://github.com/ReshadVerse) | Shared work (see below); charts B1 (Sankey), B2 (parallel coordinates), B3 (heatmap) |
| Sefa Keskin | [@sefakeskin](https://github.com/sefakeskin) | Shared work (see below); charts C1 (world map), C2 (animated bubbles), C3 (sales forecast with linear regression) |

**Shared work:** the dataset choice, project structure, shared code (`dashboard/`, `app.py`),
data preprocessing, tests and CI, the report and this documentation were planned, built and
reviewed together by all three members.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how we work together.
