import duckdb
con = duckdb.connect('analytics.duckdb')

user_id = "usr_012"  # admin
df_admin = con.execute(f"SELECT DISTINCT org_id, division FROM user_{user_id}_campaigns LIMIT 5").fetchdf()
print(df_admin.head())

# Check counts
count_admin = con.execute(f"SELECT COUNT(*) FROM user_{user_id}_campaigns").fetchone()
print(f"Admin sees {count_admin[0]} rows")

user_id = "usr_013"  # analyst
df_analyst = con.execute(f"SELECT DISTINCT org_id, division FROM user_{user_id}_campaigns LIMIT 5").fetchdf()
print(df_analyst.head())
count_analyst = con.execute(f"SELECT COUNT(*) FROM user_{user_id}_campaigns").fetchone()
print(f"Analyst sees {count_analyst[0]} rows")

user_id = "usr_003"  # viewer
df_viewer = con.execute(f"SELECT DISTINCT org_id, division FROM user_{user_id}_campaigns LIMIT 5").fetchdf()
print(df_viewer.head())
count_viewer = con.execute(f"SELECT COUNT(*) FROM user_{user_id}_campaigns").fetchone()
print(f"Viewer sees {count_viewer[0]} rows")

