import streamlit as st
import duckdb
import plotly.express as px
import plotly.graph_objects as go
from rls_security import create_rls_view

st.set_page_config(page_title="InfluencerMetrics Pro", layout="wide")

# Session-based authentication (simplified)
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Login sidebar
with st.sidebar:
    st.title("🔐 Login")
    con = duckdb.connect('analytics.duckdb')
    users = con.execute("SELECT * FROM dim_users").fetchdf()
    
    selected_user = st.selectbox("Select User", users['username'].tolist())
    
    if st.button("Login"):
        user_data = users[users['username'] == selected_user].iloc[0]
        st.session_state.user_id = user_data['user_id']
        st.session_state.user_role = user_data['role']
        st.session_state.user_org = user_data['org_id']
        st.session_state.user_division = user_data['division']
        
        # Create RLS views
        create_rls_view(
            st.session_state.user_id,
            st.session_state.user_role,
            st.session_state.user_org,
            st.session_state.user_division
        )
        st.success(f"Logged in as {selected_user}")

if st.session_state.user_id:
    st.title("📊 InfluencerMetrics Pro - Multi-Tenant Analytics")
    
    # Query user-specific data (RLS applied)
    view_name = f"user_{st.session_state.user_id}_campaigns"
    summary_view = f"user_{st.session_state.user_id}_summary"
    
    # KPI Metrics
    metrics = con.execute(f"""
        SELECT 
            COUNT(DISTINCT campaign_id) as campaigns,
            COUNT(DISTINCT post_id) as posts,
            SUM(impressions) as impressions,
            SUM(engagements) as engagements,
            AVG(engagement_rate) as avg_er
        FROM {view_name}
    """).fetchone()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Campaigns", f"{metrics[0]:,}")
    col2.metric("Posts", f"{metrics[1]:,}")
    col3.metric("Impressions", f"{metrics[2]:,}")
    col4.metric("Engagements", f"{metrics[3]:,}")
    col5.metric("Avg ER", f"{metrics[4]:.2%}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance by Platform
        platform_data = con.execute(f"""
            SELECT platform, SUM(engagements) as engagements
            FROM {view_name}
            GROUP BY platform
            ORDER BY engagements DESC
        """).fetchdf()
        
        fig = px.bar(platform_data, x='platform', y='engagements',
                     title="Engagement by Platform")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Campaign Performance
        campaign_data = con.execute(f"""
            SELECT campaign_name, total_engagements, total_spend
            FROM {summary_view}
            ORDER BY total_engagements DESC
            LIMIT 10
        """).fetchdf()
        
        fig = px.scatter(campaign_data, x='total_spend', y='total_engagements',
                        size='total_engagements', hover_data=['campaign_name'],
                        title="Campaign ROI Analysis")
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table with filters
    st.subheader("Campaign Details")
    raw_data = con.execute(f"SELECT * FROM {summary_view}").fetchdf()
    st.dataframe(raw_data, use_container_width=True)
    
else:
    st.info("👈 Please login to view analytics")