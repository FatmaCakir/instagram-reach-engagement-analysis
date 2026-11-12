# Methodology and limitations

1. Read the supplied CSV as Windows-1252 (`cp1252`) to preserve text containing nonbreaking spaces.
2. Preserve the 119 original rows and remove 17 **exact duplicate rows** for the primary 102-row analysis. Because there are no unique post IDs, exact deduplication is a transparent assumption rather than a proven correction.
3. Generate post keys `post_001` onward **after** deduplication. They are synthetic row labels, not source post IDs.
4. Derive interactions as likes + comments + shares + saves. Calculate the overall engagement rate as 100 × SUM(interactions) / SUM(impressions), not as an unweighted average of post-level rates.
5. Compute post-level descriptive rates, quartile summaries, and Spearman rank correlations. None establish causation.
6. The traffic-source components are not consistently reconciled to impression totals; reported-source shares and impression-based shares are distinct quantities. Do not treat source percentages as audited attribution.
7. Four unique records show follows > profile visits, so a follows/profile visits ratio is not a verified conversion funnel.
8. There are no dates, verified collection window, content format, audience demographics, account follower history, or unique post IDs. Do not infer trends over time, algorithm mechanics, or applicability to Instagram in 2026.
9. Check the 119-row raw versus 102-row deduplicated sensitivity analysis in the notebook.
