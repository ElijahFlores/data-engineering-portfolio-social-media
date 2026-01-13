import duckdb

con = duckdb.connect('analytics.duckdb')

# Create RLS function that filters data based on user context
def create_rls_view(user_id, user_role, user_org, user_division):
    """
    Dynamic RLS implementation - creates filtered view based on user context
    """
    
    if user_role == 'admin' and user_division is None:
        # Org admin sees all data for their org
        filter_clause = f"org_id = '{user_org}'"
    elif user_role == 'admin' and user_division:
        # Division admin sees only their division
        filter_clause = f"org_id = '{user_org}' AND (division = '{user_division}' OR division IS NULL)"
    elif user_role in ['analyst', 'viewer']:
        # Analysts/viewers see only their division
        if user_division:
            filter_clause = f"org_id = '{user_org}' AND division = '{user_division}'"
        else:
            filter_clause = f"org_id = '{user_org}'"
    else:
        filter_clause = "1=0"  # No access
    
    # Create user-specific view
    con.execute(f"""
        CREATE OR REPLACE VIEW user_{user_id}_campaigns AS
        SELECT * FROM fact_campaign_performance
        WHERE {filter_clause}
    """)
    
    con.execute(f"""
        CREATE OR REPLACE VIEW user_{user_id}_summary AS
        SELECT * FROM vw_campaign_summary
        WHERE {filter_clause}
    """)
    
    return f"user_{user_id}_campaigns", f"user_{user_id}_summary"

# Example: Create views for different user types
users = con.execute("SELECT * FROM dim_users").fetchdf()

for _, user in users.iterrows():
    views = create_rls_view(
        user['user_id'], 
        user['role'], 
        user['org_id'], 
        user['division']
    )
    print(f"✅ Created RLS views for {user['username']}: {views}")