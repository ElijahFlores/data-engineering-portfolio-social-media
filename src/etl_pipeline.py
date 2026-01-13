import duckdb
import pandas as pd
import json

# Initialize DuckDB with Parquet storage for columnar analytics
con = duckdb.connect('analytics.duckdb')

# Drop tables if they exist
con.execute("DROP TABLE IF EXISTS fact_campaign_performance")
con.execute("DROP TABLE IF EXISTS dim_users")
con.execute("DROP TABLE IF EXISTS dim_organizations")

# 1. CREATE SCHEMA 
con.execute("""
    CREATE TABLE IF NOT EXISTS dim_organizations (
        org_id VARCHAR PRIMARY KEY,
        org_name VARCHAR,
        tier VARCHAR,
        created_date DATE
    )
""")

con.execute("""
    CREATE TABLE IF NOT EXISTS dim_users (
        user_id VARCHAR PRIMARY KEY,
        username VARCHAR,
        email VARCHAR,
        org_id VARCHAR,
        role VARCHAR,
        division VARCHAR,
        FOREIGN KEY (org_id) REFERENCES dim_organizations(org_id)
    )
""")

# Key: Fact table
con.execute("""
CREATE TABLE IF NOT EXISTS fact_campaign_performance (
    post_id VARCHAR PRIMARY KEY,
    campaign_id VARCHAR,
    org_id VARCHAR,
    division VARCHAR,
    campaign_name VARCHAR,
    influencer_id VARCHAR,
    influencer_name VARCHAR,
    platform VARCHAR,
    post_timestamp TIMESTAMP,
    post_type VARCHAR,
    post_date DATE,
    impressions BIGINT,
    engagements BIGINT,
    likes BIGINT,
    comments BIGINT,
    shares BIGINT,
    saves BIGINT,
    clicks BIGINT,
    cost_usd DECIMAL(10,2),
    engagement_rate DECIMAL(5,4),
    cpe DECIMAL(10,2),
    product_category VARCHAR,
    target_age VARCHAR
)
""")


# 2. LOAD DATA (ETL Process)
orgs_df = pd.read_csv('data/organizations.csv')
users_df = pd.read_csv('data/users.csv')
campaigns_df = pd.read_json('data/campaigns.json')

# Transform: Calculate derived metrics
campaigns_df['post_date'] = pd.to_datetime(campaigns_df['post_timestamp']).dt.date
campaigns_df['engagement_rate'] = campaigns_df['engagements'] / campaigns_df['impressions']
campaigns_df['cpe'] = campaigns_df['cost_usd'] / campaigns_df['engagements']

# Load to warehouse
con.execute("INSERT INTO dim_organizations SELECT * FROM orgs_df")
con.execute("INSERT INTO dim_users SELECT * FROM users_df")
con.execute("""
INSERT INTO fact_campaign_performance (
    post_id, campaign_id, org_id, division, campaign_name,
    influencer_id, influencer_name, platform, post_timestamp, post_type,
    post_date, impressions, engagements, likes, comments, shares, saves, clicks,
    cost_usd, engagement_rate, cpe, product_category, target_age
)
SELECT
    post_id, campaign_id, org_id, division, campaign_name,
    influencer_id, influencer_name, platform, post_timestamp, post_type,
    post_date, impressions, engagements, likes, comments, shares, saves, clicks,
    cost_usd, engagement_rate, cpe, product_category, target_age
FROM campaigns_df
""")

# 3. CREATE MATERIALIZED VIEWS for Performance
con.execute("""
    CREATE OR REPLACE VIEW vw_campaign_summary AS
    SELECT 
        org_id,
        division,
        campaign_id,
        campaign_name,
        COUNT(DISTINCT post_id) as total_posts,
        COUNT(DISTINCT influencer_id) as total_influencers,
        SUM(impressions) as total_impressions,
        SUM(engagements) as total_engagements,
        AVG(engagement_rate) as avg_engagement_rate,
        SUM(cost_usd) as total_spend,
        SUM(cost_usd) / NULLIF(SUM(engagements), 0) as blended_cpe
    FROM fact_campaign_performance
    GROUP BY org_id, division, campaign_id, campaign_name
""")

print("✅ Data warehouse built successfully!")