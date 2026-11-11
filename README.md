# Exploratory Data Visualization Dashboard

An interactive dashboard built with **Python** and **Streamlit** to explore a real-world dataset
through 9 interactive visualizations and 2 machine learning models.

CEN445 Introduction to Data Visualization - Team Project (2026-2027)

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

> **TODO:** write the insight of each chart when it is finished.

| # | Chart | Type | Insight | Author |
|---|-------|------|---------|--------|
| A1 | Customer segments | K-Means clustering (advanced, ML) | | @mhakby |
| A2 | Products bought together | Network diagram (advanced) | | @mhakby |
| A3 | Top / bottom products | Bar chart | | @mhakby |
| B1 | Sales flow | Sankey diagram (advanced) | | @ReshadVerse |
| B2 | Discount, quantity, shipping cost and profit | Parallel coordinates (advanced) | | @ReshadVerse |
| B3 | Profit by sub-category and market | Heatmap | | @ReshadVerse |
| C1 | Profit by country | Choropleth map (advanced) | | @sefakeskin |
| C2 | Markets over the years | Animated bubble chart (advanced) | | @sefakeskin |
| C3 | Sales trend and forecast | Time series + linear regression (ML) | | @sefakeskin |

## Team and Contributions

| Member | GitHub | Contributions |
|--------|--------|---------------|
| | [@mhakby](https://github.com/mhakby) | Shared work (see below), charts 1-3 |
| | [@ReshadVerse](https://github.com/ReshadVerse) | Shared work (see below), charts 4-6 |
| | [@sefakeskin](https://github.com/sefakeskin) | Shared work (see below), charts 7-9 |

**Shared work:** the dataset choice, project structure, shared code (`dashboard/`, `app.py`),
data preprocessing, tests and CI, the report and this documentation were planned, built and
reviewed together by all three members.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how we work together.
