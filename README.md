# Instagram Reach & Engagement Analytics

**Data analytics bootcamp final project | Descriptive Instagram post case study**

## Research question
How are post-level engagement metrics and reported Instagram traffic sources associated with impressions, profile visits, and follows in a small Instagram dataset?

This is an **observational descriptive analysis**, not a test of Instagram's recommendation algorithm or a causal study.

## Data and methodology
- Dataset: [Instagram Reach Analysis – Case Study (Kaggle)](https://www.kaggle.com/datasets/bhanupratapbiswas/instagram-reach-analysis-case-study)
- Input: `data/raw/instagram_reach_raw.csv` (119 records; 17 exact duplicate rows removed; 102 remaining records)
- The original data has **no post dates or unique post IDs**. `post_001` etc. are generated row labels, not authentic Instagram IDs.
- There is no verified collection period, account-level follower history, format information, or audience demographics.
- The reported traffic-source counts do not consistently add up to impressions; interpret the traffic breakdown cautiously.
- Four deduplicated rows have follows exceeding profile visits. Follows/profile visits is therefore a descriptive proxy, **not** an audited conversion funnel.
- Removing exact duplicates is an assumption; without original IDs, identical rows might represent different posts. See `docs/methodology_and_limitations.md`.

## Tools
Python (Pandas, NumPy, Matplotlib), Jupyter Notebook, Tableau Public, GitHub, and PowerPoint. The project uses exploratory data analysis (EDA), descriptive statistics, and correlation analysis. SQL files are optional supplementary exercises, not required for the core analysis.

## Reproduce the analysis
From the repository root:

```bash
python -m pip install -r requirements.txt
python src/analyze.py
```

Open `notebooks/instagram_reach_analysis.ipynb` in Jupyter or VS Code and run cells in order. The notebook imports `src/analyze.py`; **keep the repository folder structure intact**.

The script creates `data/processed/tableau_posts.csv`, `data/processed/instagram_reach.sqlite`, summary tables in `outputs/`, and figures in `outputs/figures/`. SQLite examples: `sql/analysis.sql`.

## Key indicators (102 deduplicated records)
| Metric | Value |
|---|---:|
| Total impressions | 603,866 |
| Total profile visits | 5,576 |
| Total follows | 2,328 |
| Overall interactions per impression | 5.90% |

- **Interactions** = likes + comments + shares + saves.
- **Engagement per impression (%)** = 100 × total interactions / total impressions (weighted aggregate).
- **Profile visit rate (%)** = 100 × total profile visits / total impressions.
- **Follows per impression (%)** = 100 × total follows / total impressions.
- **Follows per profile visit (%)** is descriptive only; do not treat it as a validated funnel conversion rate.

## Exploratory data analysis (EDA)
The project explores distributions, post rankings, impressions versus interactions, engagement rates, impression quartiles, reported traffic sources, and profile visits versus follows. It uses descriptive statistics and Spearman correlations, **not machine learning**.

## Tableau dashboard
Open `tableau/tableu_finalprjct.twbx` in Tableau. This is the later Tableau workbook saved as `tableu_finalprjct.twbx`; it includes an embedded Tableau extract, eight worksheets, and one dashboard named **Dashboard**. The KPI values match the deduplicated dataset. The dashboard is provided **as saved**; review layout and scrolling before publishing. To reconnect manually, use `data/processed/tableau_posts.csv`.

**Public Tableau URL:** _add after publishing_

## Project structure
```text
data/raw/instagram_reach_raw.csv        Original source CSV
data/processed/                         Cleaned CSV, Tableau CSV, SQLite database
src/analyze.py                          Reproducible analysis pipeline
notebooks/instagram_reach_analysis.ipynb  Jupyter notebook
sql/analysis.sql                        SQLite queries
sql/mysql_import_example.sql           Optional MySQL-specific import example
outputs/                                Summary CSVs, quality report, figures
docs/methodology_and_limitations.md     Assumptions and caveats
docs/dashboard_guide.md                 Final Tableau checklist
tableau/tableu_finalprjct.twbx             Latest packaged Tableau workbook
presentation/Instagram_Reach_Engagement_Explained_Fatma_Cakir.pptx  Final pink presentation
```

## Interpretation and limitations
Associations do not prove why posts receive impressions, interactions, profile visits, or follows. Findings apply to this dataset only. The project cannot identify algorithmic drivers or generalize to Instagram in 2026.

## Submission status
- [x] Source data and cleaning
- [x] Python notebook and reproducible script
- [x] SQL analysis
- [x] Tableau workbook
- [ ] Final visual review of dashboard and publish to Tableau Public
- [ ] Upload repository to GitHub and paste links
- [x] Final pink presentation included (`presentation/`)

**GitHub URL:** _add after publishing_

## Updated files for this submission
- `tableau/tableu_finalprjct.twbx` — later Tableau workbook (replaces the earlier packaged workbook).
- `presentation/Instagram_Reach_Engagement_Explained_Fatma_Cakir.pptx` — final explained pink presentation.
- `notebooks/instagram_reach_analysis.ipynb` — latest notebook available in the project workspace.

The presentation contains explanatory charts based on the same analyzed dataset; do not assume every chart was exported directly from Tableau.
