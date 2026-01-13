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
1. **Materialized Views** for sub-second queries
2. **Dynamic RLS** based on user context
3. **Audit Logging** for compliance
4. **Tenant Isolation** at database level

## Run Locally
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/etl_pipeline.py
streamlit run src/dashboard.py
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