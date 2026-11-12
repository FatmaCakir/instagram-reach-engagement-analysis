
USE instagram_reach;

-- 1. Import the cleaned Instagram dataset

LOAD DATA LOCAL INFILE
'/absolute/path/to/tableau_posts.csv'
INTO TABLE posts
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @post_key,
    impressions,
    @from_home,
    @from_hashtags,
    @from_explore,
    @from_other,
    @saves,
    @comments,
    @shares,
    @likes,
    profile_visits,
    follows,
    @caption,
    @hashtags,
    interactions,
    engagement_per_impression_pct,
    @likes_rate,
    @save_rate,
    profile_visit_rate_pct,
    follows_per_impression_pct,
    @follows_per_visit,
    @traffic_sum,
    @traffic_gap,
    @traffic_reconciles,
    @follows_gt_visits,
    @caption_words,
    hashtag_count,
    @explore_pct,
    @hashtags_pct,
    @home_pct,
    @quartile
)
SET
    post_key = CAST(
        SUBSTRING(@post_key, 6) AS UNSIGNED
    ),
    traffic_source_mismatch =
        IF(@traffic_reconciles = 'True', 0, 1);


-- 2. Verify the imported records

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT post_key) AS unique_posts
FROM posts;


-- 3. Examine the first 10 posts

SELECT
    post_key,
    impressions,
    interactions,
    profile_visits,
    follows
FROM posts
LIMIT 10;


-- 4. Identify the 10 posts with highest impressions

SELECT
    post_key,
    impressions,
    interactions,
    profile_visits,
    follows
FROM posts
ORDER BY impressions DESC
LIMIT 10;


-- 5. Identify the 10 posts with highest engagement

SELECT
    post_key,
    impressions,
    interactions,
    engagement_per_impression_pct
FROM posts
ORDER BY engagement_per_impression_pct DESC
LIMIT 10;


-- 6. Examine follower acquisition

SELECT
    post_key,
    profile_visits,
    follows,
    follows_per_impression_pct
FROM posts
ORDER BY follows DESC
LIMIT 10;


-- 7. Analyze hashtag count and impressions

SELECT
    hashtag_count,
    COUNT(*) AS number_of_posts,
    ROUND(AVG(impressions), 2) AS avg_impressions
FROM posts
GROUP BY hashtag_count
ORDER BY hashtag_count;


-- 8. Identify traffic-source inconsistencies

SELECT
    COUNT(*) AS mismatched_posts
FROM posts
WHERE traffic_source_mismatch = 1;
