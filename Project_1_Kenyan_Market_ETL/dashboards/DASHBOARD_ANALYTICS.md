# Kenyan Market ETL - PowerBI Dashboard

## Dashboard Overview

This dashboard provides real-time analytics and visualization of Kenyan agricultural market data processed through our ETL pipeline.

### Dashboard Visualization

![Market Data Analytics Dashboard](dashboard_screenshot.png)

## Key Metrics Visualized

### 1. **Sum of Quantity by Date Recorded**
- Time-series analysis showing market volume trends
- Peak volumes in March 2024 reaching 4K units
- Consistent seasonal patterns throughout Q1 2024

### 2. **Sum of Price by Date Recorded**
- Price volatility analysis over time
- Maximum prices reached ~3K in February 2024
- Helps identify price fluctuation patterns for forecasting

### 3. **Sum of Quantity by Market Name**
- Top markets: Mombasa Market (18K), Garissa Market (16K), Nyeri Market (14K)
- Market concentration analysis
- Volume distribution across Kenya's major markets

### 4. **Sum of Quantity by Product Name**
- Product ranking by volume: Coffee (16K), Rice (15K), Beans (15K)
- Agricultural commodity analysis
- Supply chain insights

### 5. **Count of Data by Month**
- Data completeness monitoring
- March: 191 records, February: 165 records, January: 144 records
- Quality assurance metrics

### 6. **Count of Data by Year**
- 500 total records in 2024
- Data volume tracking for pipeline validation

## How to Use

1. **Open in PowerBI Desktop**: Use `powerbi_dashboard.pbix` file
2. **Refresh Data**: Connect to PostgreSQL database with market data
3. **Export Reports**: Use PowerBI's export functionality for stakeholder reporting
4. **Custom Filters**: Apply market, product, and date filters for deep analysis

## Data Flow to Dashboard

```
CSV Data → ETL Pipeline → PostgreSQL → PowerBI → Visualization
```

1. Extract raw data from CSV
2. Transform via Python ETL (deduplication, standardization)
3. Load to PostgreSQL with idempotent upserts
4. Connect PowerBI to live database
5. Create interactive dashboards

## Dashboard Features

- **Real-time Data**: Connected to live PostgreSQL database
- **Interactive Filters**: Filter by market, product, date range
- **Drill-down Analysis**: Click charts for detailed views
- **Export Capability**: Export visuals as PNG/PDF for reports
- **Multi-level Analytics**: Aggregation by date, market, product

## Sample Data Insights

- **Total Records Analyzed**: 500
- **Markets Covered**: 10+ major Kenyan markets
- **Products Tracked**: 10 agricultural commodities
- **Date Range**: Jan-Mar 2024
- **Data Quality**: 100% clean, deduplicated data

## Performance Metrics

- **Pipeline Execution**: 2-3 seconds for 500 records
- **Database Load**: Idempotent (safe for re-runs)
- **Dashboard Refresh**: Real-time with automatic updates
- **Query Performance**: Optimized with indexing

## Business Applications

1. **Market Intelligence**: Identify high-value markets and trends
2. **Price Forecasting**: Predict commodity price movements
3. **Supply Chain Optimization**: Optimize product distribution
4. **Agricultural Planning**: Guide planting decisions
5. **Stakeholder Reporting**: Executive dashboards for management

## Interview Talking Points

- "This dashboard demonstrates end-to-end ETL to analytics pipeline"
- "Real-time data processing with deduplication logic"
- "PostgreSQL optimization with proper indexing"
- "PowerBI integration for business intelligence"
- "Production-grade data quality and completeness"
