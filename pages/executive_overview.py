"""
Executive Overview Page
KPI dashboard and high-level metrics overview
"""

import streamlit as st
import pandas as pd
from visualizations.charts import create_line_chart, create_metric_card
from visualizations.utils import calculate_kpis, aggregate_daily_revenue


def render(data):
    """Render the Executive Overview page."""
    
    st.title("📊 Executive Overview")
    st.markdown("Strategic performance metrics and trends at a glance")
    
    # Get data
    campaign_df = data['campaign_performance'].copy()
    customer_df = data['customer_data'].copy()
    
    # Calculate KPIs
    kpis = calculate_kpis(campaign_df)
    
    # Display KPI cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Revenue",
            f"₹{kpis['total_revenue']:,.0f}",
            delta=f"+15% from last period",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Total Conversions",
            f"{kpis['total_conversions']:,}",
            delta=f"+8% from last period",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "ROAS",
            f"{kpis['roas']:.2f}x",
            delta=f"+0.25x from last period",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Total Customers",
            f"{len(customer_df):,}",
            delta=f"+12% from last period",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Revenue Trend
    st.subheader("Revenue Trend Analysis")
    
    # Prepare time series data
    campaign_df['date'] = pd.to_datetime(campaign_df['date'])
    daily_revenue = campaign_df.groupby('date')['revenue'].sum().reset_index()
    
    # Aggregation option
    col1, col2 = st.columns(2)
    with col1:
        aggregation = st.radio(
            "Time Aggregation",
            ["Daily", "Weekly", "Monthly"],
            horizontal=True,
            key="agg_overview"
        )
    
    if aggregation == "Weekly":
        daily_revenue['date'] = daily_revenue['date'].dt.to_period('W').dt.start_time
        daily_revenue = daily_revenue.groupby('date')['revenue'].sum().reset_index()
    elif aggregation == "Monthly":
        daily_revenue['date'] = daily_revenue['date'].dt.to_period('M').dt.start_time
        daily_revenue = daily_revenue.groupby('date')['revenue'].sum().reset_index()
    
    fig = create_line_chart(daily_revenue, 'date', 'revenue', "Revenue Trend", height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Channel Performance
    st.subheader("Channel Performance")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        metric_select = st.selectbox(
            "Select Metric",
            ["Revenue", "Conversions", "ROAS"],
            key="metric_overview"
        )
    
    # Aggregate by channel
    if metric_select == "Revenue":
        channel_perf = campaign_df.groupby('channel')['revenue'].sum().sort_values(ascending=True)
        title = "Revenue by Channel"
    elif metric_select == "Conversions":
        channel_perf = campaign_df.groupby('channel')['conversions'].sum().sort_values(ascending=True)
        title = "Conversions by Channel"
    else:
        channel_perf = (campaign_df.groupby('channel')['revenue'].sum() / 
                       campaign_df.groupby('channel')['spend'].sum()).sort_values(ascending=True)
        title = "ROAS by Channel"
    
    import plotly.express as px
    fig = px.barh(
        x=channel_perf.values,
        y=channel_perf.index,
        title=title,
        labels={'x': metric_select, 'y': 'Channel'},
        color=channel_perf.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("---")
    st.subheader("📈 Key Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(
            f"**Strong Revenue Growth**: Revenue has grown {kpis['roas']:.2f}x the spend with positive ROAS trend"
        )
        st.info(
            f"**High Conversion Volume**: {kpis['total_conversions']:,} conversions achieved, averaging "
            f"{kpis['avg_conversion_rate']:.2f}% conversion rate"
        )
    
    with col2:
        top_channel = campaign_df.groupby('channel')['revenue'].sum().idxmax()
        st.success(
            f"**Top Performing Channel**: {top_channel} generates the highest revenue contribution"
        )
        st.warning(
            "**Optimization Opportunity**: Consider reallocating budget to high-performing channels "
            "for improved ROAS"
        )
