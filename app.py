"""
NovaMart Marketing Analytics Dashboard
A comprehensive Streamlit application for analyzing marketing performance across multiple dimensions.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="NovaMart Marketing Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_all_data():
    """Load all CSV datasets with caching."""
    data_dir = Path(__file__).parent
    
    datasets = {}
    csv_files = [
        'campaign_performance', 'customer_data', 'product_sales',
        'lead_scoring_results', 'feature_importance', 'learning_curve',
        'geographic_data', 'channel_attribution', 'funnel_data',
        'customer_journey', 'correlation_matrix'
    ]
    
    for file in csv_files:
        try:
            datasets[file] = pd.read_csv(data_dir / f'{file}.csv')
        except FileNotFoundError:
            st.warning(f"⚠️ {file}.csv not found")
            datasets[file] = pd.DataFrame()
    
    return datasets


def render_executive_overview(data):
    """Render Executive Overview page."""
    st.title("📊 Executive Overview")
    st.markdown("Strategic performance metrics and trends at a glance")
    
    campaign_df = data['campaign_performance'].copy()
    if campaign_df.empty:
        st.error("Campaign data not available")
        return
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = campaign_df['revenue'].sum() if 'revenue' in campaign_df.columns else 0
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    
    with col2:
        total_conversions = campaign_df['conversions'].sum() if 'conversions' in campaign_df.columns else 0
        st.metric("Total Conversions", f"{total_conversions:,}")
    
    with col3:
        spend = campaign_df['spend'].sum() if 'spend' in campaign_df.columns else 1
        roas = total_revenue / spend if spend > 0 else 0
        st.metric("ROAS", f"{roas:.2f}x")
    
    with col4:
        customer_df = data['customer_data']
        customer_count = len(customer_df) if not customer_df.empty else 0
        st.metric("Total Customers", f"{customer_count:,}")
    
    st.markdown("---")
    
    # Revenue Trend
    st.subheader("Revenue Trend Analysis")
    
    if 'date' in campaign_df.columns:
        campaign_df['date'] = pd.to_datetime(campaign_df['date'])
        daily_revenue = campaign_df.groupby('date')['revenue'].sum().reset_index()
        
        st.line_chart(daily_revenue.set_index('date')['revenue'])
    
    # Channel Performance
    st.subheader("Channel Performance")
    if 'channel' in campaign_df.columns:
        channel_perf = campaign_df.groupby('channel')['revenue'].sum().sort_values(ascending=False)
        st.bar_chart(channel_perf)


def render_campaign_analytics(data):
    """Render Campaign Analytics page."""
    st.title("📈 Campaign Analytics")
    st.markdown("Analyze campaign performance across time and regions")
    
    campaign_df = data['campaign_performance'].copy()
    if campaign_df.empty:
        st.error("Campaign data not available")
        return
    
    tab1, tab2, tab3 = st.tabs(["Revenue Trends", "Regional Performance", "Campaign Types"])
    
    with tab1:
        st.subheader("Revenue Trend Over Time")
        if 'date' in campaign_df.columns and 'revenue' in campaign_df.columns:
            campaign_df['date'] = pd.to_datetime(campaign_df['date'])
            trend = campaign_df.groupby('date')['revenue'].sum()
            st.line_chart(trend)
    
    with tab2:
        st.subheader("Regional Performance")
        if 'region' in campaign_df.columns and 'revenue' in campaign_df.columns:
            regional = campaign_df.groupby('region')['revenue'].sum().sort_values(ascending=False)
            st.bar_chart(regional)
    
    with tab3:
        st.subheader("Campaign Type Analysis")
        if 'campaign_type' in campaign_df.columns and 'spend' in campaign_df.columns:
            campaigns = campaign_df.groupby('campaign_type')['spend'].sum().sort_values(ascending=False)
            st.bar_chart(campaigns)


def render_customer_insights(data):
    """Render Customer Insights page."""
    st.title("👥 Customer Insights")
    st.markdown("Understand customer segments, demographics, and value distribution")
    
    customer_df = data['customer_data'].copy()
    if customer_df.empty:
        st.error("Customer data not available")
        return
    
    tab1, tab2, tab3 = st.tabs(["Demographics", "Value Analysis", "Satisfaction"])
    
    with tab1:
        st.subheader("Customer Age Distribution")
        if 'age' in customer_df.columns:
            st.histogram(customer_df['age'], bins=30, title="Age Distribution")
    
    with tab2:
        st.subheader("Lifetime Value Analysis")
        if 'segment' in customer_df.columns and 'ltv' in customer_df.columns:
            ltv_by_segment = customer_df.groupby('segment')['ltv'].mean().sort_values(ascending=False)
            st.bar_chart(ltv_by_segment)
    
    with tab3:
        st.subheader("Satisfaction Metrics")
        if 'nps_category' in customer_df.columns:
            nps_dist = customer_df['nps_category'].value_counts()
            st.bar_chart(nps_dist)


def render_product_performance(data):
    """Render Product Performance page."""
    st.title("🛍️ Product Performance")
    st.markdown("Analyze product sales hierarchy and profitability")
    
    product_df = data['product_sales'].copy()
    if product_df.empty:
        st.error("Product data not available")
        return
    
    tab1, tab2 = st.tabs(["Category Performance", "Regional Analysis"])
    
    with tab1:
        st.subheader("Sales by Category")
        if 'category' in product_df.columns and 'sales' in product_df.columns:
            category_sales = product_df.groupby('category')['sales'].sum().sort_values(ascending=False)
            st.bar_chart(category_sales)
    
    with tab2:
        st.subheader("Regional Product Performance")
        if 'region' in product_df.columns and 'sales' in product_df.columns:
            region_sales = product_df.groupby('region')['sales'].sum().sort_values(ascending=False)
            st.bar_chart(region_sales)


def render_geographic_analysis(data):
    """Render Geographic Analysis page."""
    st.title("🗺️ Geographic Analysis")
    st.markdown("Analyze performance across regions and states")
    
    geo_df = data['geographic_data'].copy()
    if geo_df.empty:
        st.error("Geographic data not available")
        return
    
    st.subheader("State-wise Performance")
    
    if 'state' in geo_df.columns and 'revenue' in geo_df.columns:
        geo_sorted = geo_df.sort_values('revenue', ascending=True)
        st.bar_chart(geo_sorted.set_index('state')['revenue'])
    
    st.subheader("Detailed Metrics")
    st.dataframe(geo_df)


def render_attribution_funnel(data):
    """Render Attribution & Funnel page."""
    st.title("🔗 Attribution & Funnel Analysis")
    st.markdown("Understand customer journey and channel attribution")
    
    tab1, tab2 = st.tabs(["Conversion Funnel", "Attribution Models"])
    
    with tab1:
        st.subheader("Marketing Funnel")
        funnel_df = data['funnel_data']
        if not funnel_df.empty and 'stage' in funnel_df.columns and 'visitors' in funnel_df.columns:
            st.bar_chart(funnel_df.set_index('stage')['visitors'])
    
    with tab2:
        st.subheader("Attribution Model Comparison")
        attr_df = data['channel_attribution']
        if not attr_df.empty:
            st.dataframe(attr_df)


def render_ml_evaluation(data):
    """Render ML Model Evaluation page."""
    st.title("🤖 ML Model Evaluation")
    st.markdown("Analyze lead scoring model performance")
    
    tab1, tab2, tab3 = st.tabs(["Model Performance", "Feature Importance", "Learning Curve"])
    
    with tab1:
        st.subheader("Model Metrics")
        lead_df = data['lead_scoring_results']
        if not lead_df.empty:
            st.metric("Predictions Loaded", len(lead_df))
    
    with tab2:
        st.subheader("Feature Importance")
        feat_df = data['feature_importance']
        if not feat_df.empty and 'feature' in feat_df.columns and 'importance' in feat_df.columns:
            st.bar_chart(feat_df.set_index('feature')['importance'])
    
    with tab3:
        st.subheader("Learning Curve")
        learn_df = data['learning_curve']
        if not learn_df.empty:
            st.dataframe(learn_df)


def main():
    """Main application entry point."""
    
    # Load data
    data = load_all_data()
    
    # Sidebar navigation
    st.sidebar.title("🎯 NovaMart Analytics")
    st.sidebar.markdown("---")
    
    pages = {
        "📊 Executive Overview": render_executive_overview,
        "📈 Campaign Analytics": render_campaign_analytics,
        "👥 Customer Insights": render_customer_insights,
        "🛍️ Product Performance": render_product_performance,
        "🗺️ Geographic Analysis": render_geographic_analysis,
        "🔗 Attribution & Funnel": render_attribution_funnel,
        "🤖 ML Model Evaluation": render_ml_evaluation,
    }
    
    selected_page = st.sidebar.radio("Navigation", list(pages.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
    **NovaMart Dashboard**
    
    Interactive analytics for omnichannel retail marketing performance.
    
    📧 Questions? Contact the Analytics Team
    """
    )
    
    # Render selected page
    page_func = pages[selected_page]
    page_func(data)


if __name__ == "__main__":
    main()
