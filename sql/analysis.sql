-- SQLite examples; generated database: data/processed/instagram_reach.sqlite
-- These are associations within this dataset, not causal findings.
SELECT COUNT(*) AS posts,
 SUM(impressions) AS total_impressions,
 SUM(interactions) AS total_interactions,
 ROUND(100.0 * SUM(interactions) / NULLIF(SUM(impressions),0), 2) AS engagement_per_impression_pct,
 ROUND(100.0 * SUM(profile_visits) / NULLIF(SUM(impressions),0), 2) AS profile_visit_rate_pct,
 ROUND(100.0 * SUM(follows) / NULLIF(SUM(impressions),0), 2) AS follows_per_impression_pct
FROM posts;

-- Highest-impression posts; no date or post URL is supplied by the source.
SELECT post_key, impressions, interactions, profile_visits, follows,
 ROUND(engagement_per_impression_pct,2) AS engagement_per_impression_pct
FROM posts ORDER BY impressions DESC LIMIT 10;

-- Correlation-friendly segmentation; quartiles use NTILE.
WITH ranked AS (
 SELECT *, NTILE(4) OVER (ORDER BY impressions) AS impression_quartile FROM posts
)
SELECT impression_quartile, COUNT(*) AS posts,
 ROUND(AVG(impressions),1) AS avg_impressions,
 ROUND(AVG(engagement_per_impression_pct),2) AS mean_post_engagement_per_impression_pct,
 ROUND(AVG(profile_visit_rate_pct),2) AS mean_profile_visit_rate_pct
FROM ranked GROUP BY impression_quartile ORDER BY impression_quartile;

-- Data integrity: some source components do not sum exactly to impressions.
SELECT COUNT(*) AS traffic_mismatch_rows,
 SUM(CASE WHEN traffic_sum > impressions THEN 1 ELSE 0 END) AS traffic_exceeds_impressions_rows,
 SUM(CASE WHEN follows > profile_visits THEN 1 ELSE 0 END) AS follows_exceed_visits_rows
FROM posts WHERE traffic_sum <> impressions;

-- Caption / hashtag length correlation is assessed in Python; SQL summary by hashtag tiers.
SELECT CASE WHEN hashtag_count < 10 THEN '0-9' WHEN hashtag_count < 20 THEN '10-19' ELSE '20+' END AS hashtag_tier,
 COUNT(*) AS posts, ROUND(AVG(impressions),1) AS avg_impressions,
 ROUND(AVG(engagement_per_impression_pct),2) AS mean_engagement_rate
FROM posts GROUP BY hashtag_tier ORDER BY hashtag_tier;
