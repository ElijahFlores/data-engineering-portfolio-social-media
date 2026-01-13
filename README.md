# InfluencerMetrics Pro - Multi-Tenant Analytics Platform

A production-grade data engineering portfolio demonstrating:
- ✅ Multi-tenant data architecture with RLS
- ✅ Columnar database optimization (DuckDB)
- ✅ Real-time analytics dashboard
- ✅ ETL pipeline with data quality
- ✅ Session-based access control

## Tech Stack
- **Database**: DuckDB (columnar, analytical)
- **ETL**: Python, Pandas
- **Security**: Row-Level Security (RLS), RBAC
- **BI**: Streamlit, Plotly
- **Storage**: Parquet (optimized columnar format)

## Key Features Demonstrated
1. **Partitioned Tables** by org_id and date
2. **Materialized Views** for sub-second queries
3. **Dynamic RLS** based on user context
4. **Audit Logging** for compliance
5. **Tenant Isolation** at database level

## Run Locally
```bash
pip install -r requirements.txt
python generate_data.py
python etl_pipeline.py
streamlit run dashboard.py
```

## Performance Metrics
- 10,000+ records processed
- Sub-second query response (<500ms)
- Multi-tenant isolation verified
- Handles concurrent users

## Security Implementation
- Row-Level Security enforced
- Role-Based Access Control (Admin/Analyst/Viewer)
- Division-level data segmentation
- Session-based context management