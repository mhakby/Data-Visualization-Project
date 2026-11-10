# How We Work

## Who owns what

| Area | Owner | Notes |
|------|-------|-------|
| `app.py`, `dashboard/`, `scripts/`, `tests/`, `.github/`, docs | Whole team | Shared code. Changes are agreed in an issue first. |
| `members/mhakby/` | @mhakby | |
| `members/reshadverse/` | @ReshadVerse | |
| `members/sefakeskin/` | @sefakeskin | |

**In your chart work, only edit files inside your own folder.** If you need something in the
shared code (a new column, a fix in the cleaning step, a new color), open an issue first so the
team can agree on it, then make the change in a separate pull request.

## Workflow

1. **Pick your issue.** Every task is an issue assigned to someone.
2. **Update `main` and create a branch** named `<username>/<short-description>`:
   ```bash
   git switch main
   git pull
   git switch -c reshadverse/sankey-chart
   ```
3. **Work and commit** in small steps. Write short commit messages that say what you did:
   `Add sankey chart`, `Fix legend title in treemap`.
4. **Check your code** before pushing:
   ```bash
   ruff check .
   pytest
   streamlit run app.py
   ```
5. **Push and open a pull request** to `main`. Write `Closes #<issue number>` in the
   description so the issue closes automatically when the PR is merged.
6. **Wait for the checks and a review.** GitHub Actions runs `ruff` and `pytest` on every PR.
   At least one teammate approves before merging.

Never push directly to `main`.

## Adding a chart

1. Copy `members/_template/chart_template.py` into your folder and rename it,
   e.g. `members/reshadverse/chart_sankey.py`.
2. Fill in `TITLE`, `INSIGHT` and the `render(df)` function.
3. Add it to the `CHARTS` list in your folder's `__init__.py`:
   ```python
   from members.reshadverse import chart_sankey

   TAB_TITLE = "Flows & Relationships"
   CHARTS = [chart_sankey]
   ```
4. Run the app. Your chart appears in your tab.

### Chart rules

- `df` in `render(df)` is **already filtered** by the sidebar. Do not load the data again.
- Do not change `df` in place. If you need a new column, work on a copy: `df = df.copy()`.
- **Widget keys must start with your username**, e.g. `key="reshadverse_year"`.
  Streamlit crashes when two widgets have the same key.
- Use the shared colors from `dashboard/theme.py` and call `style_figure(fig)`.
- Every chart needs a title, axis labels and a legend title (if it has a legend).
- Each chart must show a **different insight** and have some interactivity
  (hover tooltips, zoom, a slider, a dropdown, ...).
- Write your findings in your `NOTES.md`. We use them for the report and the presentation.

## Issues

| Type | Use it for |
|------|-----------|
| **Chart task** | One chart = one issue, assigned to its author |
| **Decision** | Team decisions (dataset, chart split, ...). Everyone comments, then we close it with the final decision written in the last comment. |
| **Bug report** | Something is broken |
