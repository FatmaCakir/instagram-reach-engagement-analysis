# Tableau final review checklist

The included `.twbx` is the **actual saved workbook**, with a packaged Tableau extract. No need to recreate the dashboard.

1. Open `tableau/tableu_finalprjct.twbx` in Tableau Public.
2. Confirm KPI cards show **603,866 impressions**, **5,576 profile visits**, **2,328 follows**, and **5.90% engagement**.
3. Review card alignment and check that no values show `##`. The source workbook uses floating dashboard objects, so the appearance may differ across screen sizes.
4. Scroll down to inspect the lower two charts (Profile Visits vs. Follows and Instagram Traffic Sources).
5. Verify axis titles, tooltip readability, and consistent chart naming.
6. Save/publish to Tableau Public when comfortable making the workbook and packaged data publicly accessible.
7. Copy the public Tableau link into the README and GitHub repository description.

Note: The workbook's original connection also references a local file path, but the `.twbx` contains an embedded `.hyper` extract. If the extract does not load, regenerate `data/processed/tableau_posts.csv` using `python src/analyze.py` and reconnect the data source.
