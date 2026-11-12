"""Reproducible descriptive Instagram post analysis. Run from any directory.

Source CSV is Windows-1252 encoded; it contains no post IDs or dates.
Post keys are generated labels, not actual Instagram post IDs.
"""
from pathlib import Path
import json
import re
import sqlite3
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'data/raw/instagram_reach_raw.csv'
PROCESSED = ROOT / 'data/processed'
OUTPUT = ROOT / 'outputs'
FIGURES = OUTPUT / 'figures'

RENAME = {
    'Impressions': 'impressions', 'From Home': 'from_home',
    'From Hashtags': 'from_hashtags', 'From Explore': 'from_explore',
    'From Other': 'from_other', 'Saves': 'saves',
    'Comments': 'comments', 'Shares': 'shares', 'Likes': 'likes',
    'Profile Visits': 'profile_visits', 'Follows': 'follows',
    'Caption': 'caption', 'Hashtags': 'hashtags',
}

def _rate(num, den):
    return 100 * num / den if den else np.nan

def load_prepare():
    raw = pd.read_csv(RAW, encoding='cp1252')
    missing = sorted(set(RENAME) - set(raw.columns))
    if missing:
        raise ValueError(f'Missing required CSV columns: {missing}')
    exact_duplicates = int(raw.duplicated().sum())
    posts = raw.drop_duplicates().copy().reset_index(drop=True).rename(columns=RENAME)
    for col in RENAME.values():
        if col not in ('caption', 'hashtags'):
            posts[col] = pd.to_numeric(posts[col], errors='coerce')
    posts['post_key'] = [f'post_{i:03d}' for i in range(1, len(posts)+1)]
    posts['interactions'] = posts[['likes','comments','shares','saves']].sum(axis=1)
    posts['engagement_per_impression_pct'] = 100 * posts['interactions'] / posts['impressions'].replace(0, np.nan)
    posts['likes_rate'] = 100 * posts['likes'] / posts['impressions'].replace(0, np.nan)
    posts['save_rate'] = 100 * posts['saves'] / posts['impressions'].replace(0, np.nan)
    posts['profile_visit_rate_pct'] = 100 * posts['profile_visits'] / posts['impressions'].replace(0, np.nan)
    posts['follows_per_impression_pct'] = 100 * posts['follows'] / posts['impressions'].replace(0, np.nan)
    posts['follows_per_visit_pct'] = 100 * posts['follows'] / posts['profile_visits'].replace(0, np.nan)
    traffic_cols = ['from_home','from_hashtags','from_explore','from_other']
    posts['traffic_sum'] = posts[traffic_cols].sum(axis=1)
    posts['traffic_gap'] = posts['impressions'] - posts['traffic_sum']
    posts['traffic_reconciles'] = posts['traffic_gap'] == 0
    posts['follows_gt_visits'] = posts['follows'] > posts['profile_visits']
    posts['caption_words'] = posts['caption'].fillna('').astype(str).str.split().str.len()
    posts['hashtag_count'] = posts['hashtags'].fillna('').astype(str).str.count('#')
    for c in traffic_cols:
        posts[c+'_pct'] = 100 * posts[c] / posts['impressions'].replace(0, np.nan)
    posts['impression_quartile'] = pd.qcut(posts['impressions'].rank(method='first'), 4, labels=['Q1','Q2','Q3','Q4'])
    quality = {
        'raw_rows': int(len(raw)),
        'exact_duplicates_removed': exact_duplicates,
        'unique_rows': int(len(posts)),
        'missing_cells_after_cleaning': int(posts[list(RENAME.values())].isna().sum().sum()),
        'traffic_mismatch_rows': int((~posts['traffic_reconciles']).sum()),
        'traffic_exceeds_impressions_rows': int((posts['traffic_sum'] > posts['impressions']).sum()),
        'follows_exceed_profile_visits_rows': int(posts['follows_gt_visits'].sum()),
        'post_ids_are_generated': True,
        'original_post_dates_available': False,
    }
    return raw, posts, quality

def make_results(posts):
    PROCESSED.mkdir(parents=True,exist_ok=True)
    FIGURES.mkdir(parents=True,exist_ok=True)
    kpis = {
        'post_records': int(len(posts)),
        'total_impressions': int(posts['impressions'].sum()),
        'total_interactions': int(posts['interactions'].sum()),
        'total_profile_visits': int(posts['profile_visits'].sum()),
        'total_follows': int(posts['follows'].sum()),
        'engagement_per_impression_pct': round(_rate(posts['interactions'].sum(),posts['impressions'].sum()),2),
        'profile_visit_rate_pct': round(_rate(posts['profile_visits'].sum(),posts['impressions'].sum()),2),
        'follows_per_impression_pct': round(_rate(posts['follows'].sum(),posts['impressions'].sum()),2),
        'follows_per_profile_visit_pct_descriptive_only': round(_rate(posts['follows'].sum(),posts['profile_visits'].sum()),2),
    }
    traffic = pd.DataFrame({'source':['Home','Hashtags','Explore','Other'],
      'reported_count':[int(posts[c].sum()) for c in ['from_home','from_hashtags','from_explore','from_other']]})
    traffic['pct_of_reported_source_total'] = (100*traffic['reported_count']/traffic['reported_count'].sum()).round(2)
    quartiles = posts.groupby('impression_quartile',observed=True).agg(
      posts=('post_key','count'),avg_impressions=('impressions','mean'),
      mean_post_engagement_per_impression_pct=('engagement_per_impression_pct','mean'),
      mean_profile_visit_rate_pct=('profile_visit_rate_pct','mean')).round(2).reset_index()
    numeric = ['impressions','interactions','likes','comments','shares','saves','profile_visits','follows','caption_words','hashtag_count','engagement_per_impression_pct']
    cor = posts[numeric].corr(method='spearman')
    cor.to_csv(OUTPUT/'spearman_correlations.csv')
    pd.DataFrame([kpis]).to_csv(OUTPUT/'kpis.csv',index=False)
    traffic.to_csv(OUTPUT/'traffic_composition.csv',index=False)
    quartiles.to_csv(OUTPUT/'impression_quartiles.csv',index=False)
    posts.to_csv(PROCESSED/'instagram_reach_cleaned.csv',index=False)
    posts.to_csv(PROCESSED/'tableau_posts.csv',index=False)
    with sqlite3.connect(PROCESSED/'instagram_reach.sqlite') as db:
        posts.to_sql('posts',db,if_exists='replace',index=False)
    def finish(name):
        plt.tight_layout();plt.savefig(FIGURES/f'{name}.png',dpi=140,bbox_inches='tight');plt.close()
    plt.figure(figsize=(8,4.5));plt.hist(posts['impressions'],bins=18)
    plt.title('Post impressions distribution');plt.xlabel('Impressions');plt.ylabel('Post count');finish('impressions_distribution')
    plt.figure(figsize=(8,4.5));plt.scatter(posts['impressions'],posts['interactions'],alpha=.6)
    plt.title('Interactions vs impressions');plt.xlabel('Impressions');plt.ylabel('Interactions');finish('interactions_vs_impressions')
    plt.figure(figsize=(8,4.5));plt.bar(traffic['source'],traffic['reported_count'])
    plt.title('Reported Instagram traffic sources');plt.ylabel('Reported count');finish('traffic_sources')
    plt.figure(figsize=(8,4.5));plt.scatter(posts['profile_visits'],posts['follows'],alpha=.6)
    plt.title('Follows vs profile visits');plt.xlabel('Profile visits');plt.ylabel('Follows');finish('visits_vs_follows')
    results = {'kpis':kpis,'spearman_impressions_likes':float(cor.loc['impressions','likes'])}
    return results,traffic,quartiles

def main():
    raw,posts,quality=load_prepare()
    results,_,_=make_results(posts)
    (OUTPUT/'data_quality_report.json').write_text(json.dumps(quality,indent=2),encoding='utf-8')
    print('Data quality:',json.dumps(quality,indent=2))
    print('KPIs:',json.dumps(results['kpis'],indent=2))
    print('Created Tableau-ready CSV, SQLite database, figures, and summary CSVs.')

if __name__ == '__main__':
    main()
