import pandas as pd
import json
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

# Generate 3 organizations
organizations = [
    {"org_id": f"org_{i:03d}", "org_name": fake.company(), 
     "tier": random.choice(["enterprise", "business"]),
     "created_date": fake.date_between(start_date='-1y', end_date='today')}
    for i in range(1, 4)
]

# Generate 15 users across orgs
users = []
divisions = ["north_america", "emea", "apac", None]
for i in range(1, 16):
    org = random.choice(organizations)
    users.append({
        "user_id": f"usr_{i:03d}",
        "username": fake.user_name(),
        "email": fake.email(),
        "org_id": org["org_id"],
        "role": random.choice(["admin", "analyst", "viewer"]),
        "division": random.choice(divisions) if org["tier"] == "enterprise" else None
    })

# Generate 10,000 campaign posts
campaigns = []
platforms = ["instagram", "tiktok", "youtube", "twitter"]
post_types = ["post", "reel", "story", "video"]

for i in range(10000):
    org = random.choice(organizations)
    post_date = fake.date_time_between(start_date='-90d', end_date='now')
    
    impressions = random.randint(1000, 500000)
    engagements = int(impressions * random.uniform(0.02, 0.15))
    
    campaigns.append({
        "campaign_id": f"camp_{random.randint(1, 50):03d}",
        "org_id": org["org_id"],
        "division": random.choice(divisions) if org["tier"] == "enterprise" else None,
        "campaign_name": f"{fake.catch_phrase()} Campaign",
        "influencer_id": f"inf_{random.randint(1, 200):03d}",
        "influencer_name": f"@{fake.user_name()}",
        "platform": random.choice(platforms),
        "post_id": f"post_{i:06d}",
        "post_timestamp": post_date.isoformat(),
        "post_type": random.choice(post_types),
        "impressions": impressions,
        "engagements": engagements,
        "likes": int(engagements * 0.7),
        "comments": int(engagements * 0.15),
        "shares": int(engagements * 0.10),
        "saves": int(engagements * 0.05),
        "clicks": int(impressions * random.uniform(0.01, 0.05)),
        "cost_usd": random.randint(500, 15000),
        "product_category": random.choice(["apparel", "beauty", "tech", "food"]),
        "target_age": random.choice(["18-24", "25-34", "35-44", "45+"])
    })

# Save to files
pd.DataFrame(organizations).to_csv('data/organizations.csv', index=False)
pd.DataFrame(users).to_csv('data/users.csv', index=False)
pd.DataFrame(campaigns).to_json('data/campaigns.json', orient='records', indent=2)