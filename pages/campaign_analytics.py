"""
Campaign Analytics Page
Temporal and comparison visualizations for campaign performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from visualizations.charts import (
    create_line_chart, create_area_chart, create_bar_chart,
    create_altair_heatmap
)


def render(data):
    """Render the Campaign Analytics page."""
    
    st.title("📈 Campaign Analytics")
    st.markdown("Analyze campaign performance across time, regions, and campaign types")
    
    campaign_df = data['campaign_performance'].copy()
    campaign_df['date'] = pd.to_datetime(campaign_df['date'])
    
    # Tab selection
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Revenue Trends",
        "🌍 Regional Performance",
        "💰 Campaign Type Analysis",
        "📅 Calendar Heatmap"
    ])
    
    with tab1:
        st.subheader("Revenue Trend Over Time")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            agg = st.radio("Aggregation", ["Daily", "Weekly", "Monthly"], horizontal=True, key="agg_camp")
        
        with col2:
            st.write("")
        
        with col3:
            st.write("")
        
        # Prepare data
        revenue_ts = campaign_df.groupby('date')['revenue'].sum().reset_index()
        
        if agg == "Weekly":
            revenue_ts['date'] = revenue_ts['date'].dt.to_period('W').dt.start_time
            revenue_ts = revenue_ts.groupby('date')['revenue'].sum().reset_index()
        elif agg == "Monthly":
            revenue_ts['date'] = revenue_ts['date'].dt.to_period('M').dt.start_time
            revenue_ts = revenue_ts.groupby('date')['revenue'].sum().reset_index()
        
        fig = create_line_chart(revenue_ts, 'date', 'revenue', "Revenue Trend", height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: Clear upward trend with strong seasonality visible. Holiday seasons (Q4) show significant peaks.")
    
    with tab2:
        st.subheader("Regional Performance by Quarter")
        
        col1, col2 = st.columns(2)
        
        with col1:
            year_select = st.selectbox("Select Year", campaign_df['date'].dt.year.unique(), key="year_region")
        
        with col2:
            st.write("")
        
        # Calculate quarter
        region_quarterly = campaign_df[campaign_df['date'].dt.year == year_select].copy()
        region_quarterly['quarter'] = region_quarterly['date'].dt.quarter
        region_quarterly = region_quarterly.groupby(['region', 'quarter'])['revenue'].sum().reset_index()
        
        fig = px.bar(
            region_quarterly,
            x='quarter',
            y='revenue',
            color='region',
            barmode='group',
            title=f"Regional Revenue by Quarter ({year_select})",
            labels={'quarter': 'Quarter', 'revenue': 'Revenue (₹)'}
        )
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: West and South regions consistently outperform. Q4 shows significant festive season boost.")
    
    with tab3:
        st.subheader("Campaign Type Budget Allocation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            view_type = st.radio("View Type", ["Absolute", "100% Stacked"], horizontal=True, key="view_camp")
        
        with col2:
            st.write("")
        
        # Aggregate by campaign type and month
        campaign_df['month'] = campaign_df['date'].dt.to_period('M').astype(str)
        campaign_type_monthly = campaign_df.groupby(['month', 'campaign_type'])['spend'].sum().reset_index()
        
        if view_type == "Absolute":
            fig = px.bar(
                campaign_type_monthly,
                x='month',
                y='spend',
                color='campaign_type',
                barmode='stack',
                title="Monthly Campaign Type Spend Distribution"
            )
        else:
            fig = px.bar(
                campaign_type_monthly,
                x='month',
                y='spend',
                color='campaign_type',
                barmode='relative',
                barnorm='percent',
                title="Monthly Campaign Type Spend Distribution (100% Stacked)"
            )
        
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: Lead Generation campaigns consume the largest budget. Seasonal Sale campaigns spike during Q4 (festive season).")
    
    with tab4:
        st.subheader("Daily Performance Calendar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            year = st.selectbox("Select Year", campaign_df['date'].dt.year.unique(), key="year_cal")
        
        with col2:
            metric = st.selectbox("Select Metric", ["Revenue", "Conversions", "Spend"], key="metric_cal")
        
        # Filter data
        cal_data = campaign_df[campaign_df['date'].dt.year == year].copy()
        cal_data['day_of_week'] = cal_data['date'].dt.day_name()
        cal_data['week'] = cal_data['date'].dt.isocalendar().week
        
        if metric == "Revenue":
            cal_agg = cal_data.groupby(['week', 'day_of_week'])['revenue'].sum().reset_index()
            metric_col = 'revenue'
        elif metric == "Conversions":
            cal_agg = cal_data.groupby(['week', 'day_of_week'])['conversions'].sum().reset_index()
            metric_col = 'conversions'
        else:
            cal_agg = cal_data.groupby(['week', 'day_of_week'])['spend'].sum().reset_index()
            metric_col = 'spend'
        
        # Order days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cal_agg['day_of_week'] = pd.Categorical(cal_agg['day_of_week'], categories=day_order, ordered=True)
        cal_agg = cal_agg.sort_values('day_of_week')
        
        fig = px.density_heatmap(
            cal_agg,
            x='day_of_week',
            y='week',
            nbinsx=7,
            nbinsy=52,
            color_continuous_scale='Blues',
            title=f"{metric} Heatmap by Day and Week ({year})"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: Clear weekday vs weekend patterns. Festive periods (Oct-Nov) show intense activity intensity.")
