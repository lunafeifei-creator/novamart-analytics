"""
NovaMart Marketing Analytics Dashboard
A comprehensive Streamlit application for analyzing marketing performance across multiple dimensions.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
            datasets[file] = pd.DataFrame()
    
    return datasets


def render_executive_overview(data):
    """Render Executive Overview page."""
    st.title("📊 Executive Overview")
    st.markdown("Strategic performance metrics and trends at a glance")
    
    campaign_df = data['campaign_performance'].copy()
    customer_df = data['customer_data'].copy()
    
    if campaign_df.empty:
        st.warning("⚠️ Campaign data not available")
        return
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = campaign_df['revenue'].sum() if 'revenue' in campaign_df.columns else 0
    total_conversions = campaign_df['conversions'].sum() if 'conversions' in campaign_df.columns else 0
    spend = campaign_df['spend'].sum() if 'spend' in campaign_df.columns else 1
    roas = total_revenue / spend if spend > 0 else 0
    customer_count = len(customer_df) if not customer_df.empty else 0
    
    with col1:
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}", delta="+15% from last month")
    
    with col2:
        st.metric("Total Conversions", f"{total_conversions:,}", delta="+8% from last month")
    
    with col3:
        st.metric("ROAS", f"{roas:.2f}x", delta="+0.25x from last month")
    
    with col4:
        st.metric("Total Customers", f"{customer_count:,}", delta="+12% from last month")
    
    st.markdown("---")
    
    # Revenue Trend
    st.subheader("Revenue Trend Analysis")
    
    if 'date' in campaign_df.columns and 'revenue' in campaign_df.columns:
        campaign_df['date'] = pd.to_datetime(campaign_df['date'], errors='coerce')
        daily_revenue = campaign_df.groupby('date')['revenue'].sum().reset_index().dropna()
        
        if not daily_revenue.empty:
            fig = px.line(
                daily_revenue,
                x='date',
                y='revenue',
                title="Daily Revenue Trend",
                labels={'date': 'Date', 'revenue': 'Revenue (₹)'},
                markers=True
            )
            fig.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Channel Performance
    st.subheader("Channel Performance")
    if 'channel' in campaign_df.columns and 'revenue' in campaign_df.columns:
        channel_perf = campaign_df.groupby('channel')['revenue'].sum().sort_values(ascending=True)
        
        fig = px.barh(
            x=channel_perf.values,
            y=channel_perf.index,
            title="Revenue by Channel",
            labels={'x': 'Revenue (₹)', 'y': 'Channel'},
            color=channel_perf.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def render_campaign_analytics(data):
    """Render Campaign Analytics page."""
    st.title("📈 Campaign Analytics")
    st.markdown("Analyze campaign performance across time and regions")
    
    campaign_df = data['campaign_performance'].copy()
    if campaign_df.empty:
        st.warning("⚠️ Campaign data not available")
        return
    
    tab1, tab2, tab3 = st.tabs(["Revenue Trends", "Regional Performance", "Campaign Types"])
    
    with tab1:
        st.subheader("Revenue Trend Over Time")
        if 'date' in campaign_df.columns and 'revenue' in campaign_df.columns:
            campaign_df['date'] = pd.to_datetime(campaign_df['date'], errors='coerce')
            daily_revenue = campaign_df.groupby('date')['revenue'].sum().reset_index().dropna()
            
            if not daily_revenue.empty:
                fig = px.line(
                    daily_revenue,
                    x='date',
                    y='revenue',
                    title="Revenue Over Time",
                    markers=True
                )
                fig.update_layout(height=450, hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Regional Performance")
        if 'region' in campaign_df.columns and 'revenue' in campaign_df.columns:
            regional = campaign_df.groupby('region')['revenue'].sum().sort_values(ascending=False)
            
            fig = px.bar(
                x=regional.index,
                y=regional.values,
                title="Revenue by Region",
                labels={'x': 'Region', 'y': 'Revenue (₹)'},
                color=regional.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Campaign Type Analysis")
        if 'campaign_type' in campaign_df.columns and 'spend' in campaign_df.columns:
            campaigns = campaign_df.groupby('campaign_type')['spend'].sum().sort_values(ascending=False)
            
            fig = px.pie(
                values=campaigns.values,
                names=campaigns.index,
                title="Campaign Type Budget Distribution"
            )
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)


def render_customer_insights(data):
    """Render Customer Insights page."""
    st.title("👥 Customer Insights")
    st.markdown("Understand customer segments, demographics, and value distribution")
    
    customer_df = data['customer_data'].copy()
    if customer_df.empty:
        st.warning("⚠️ Customer data not available")
        return
    
    tab1, tab2, tab3 = st.tabs(["Demographics", "Value Analysis", "Satisfaction"])
    
    with tab1:
        st.subheader("Customer Age Distribution")
        if 'age' in customer_df.columns:
            fig = px.histogram(
                customer_df,
                x='age',
                nbins=30,
                title="Customer Age Distribution",
                labels={'age': 'Age', 'count': 'Count'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Lifetime Value by Segment")
        if 'segment' in customer_df.columns and 'ltv' in customer_df.columns:
            fig = px.box(
                customer_df,
                x='segment',
                y='ltv',
                title="Lifetime Value Distribution by Segment",
                color='segment'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistics
            stats = customer_df.groupby('segment')['ltv'].agg(['mean', 'median', 'count'])
            st.dataframe(stats, use_container_width=True)
    
    with tab3:
        st.subheader("Satisfaction Metrics")
        if 'nps_category' in customer_df.columns:
            nps_dist = customer_df['nps_category'].value_counts()
            
            fig = px.bar(
                x=nps_dist.index,
                y=nps_dist.values,
                title="Customer Distribution by NPS Category",
                labels={'x': 'NPS Category', 'y': 'Count'},
                color=nps_dist.values,
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


def render_product_performance(data):
    """Render Product Performance page."""
    st.title("🛍️ Product Performance")
    st.markdown("Analyze product sales hierarchy and profitability")
    
    product_df = data['product_sales'].copy()
    if product_df.empty:
        st.warning("⚠️ Product data not available")
        return
    
    tab1, tab2 = st.tabs(["Category Performance", "Regional Analysis"])
    
    with tab1:
        st.subheader("Sales by Category")
        if 'category' in product_df.columns and 'sales' in product_df.columns:
            category_sales = product_df.groupby('category')['sales'].sum().sort_values(ascending=False)
            
            fig = px.bar(
                x=category_sales.index,
                y=category_sales.values,
                title="Sales by Product Category",
                labels={'x': 'Category', 'y': 'Sales (₹)'},
                color=category_sales.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Regional Product Performance")
        if 'region' in product_df.columns and 'sales' in product_df.columns:
            region_sales = product_df.groupby('region')['sales'].sum().sort_values(ascending=False)
            
            fig = px.bar(
                x=region_sales.index,
                y=region_sales.values,
                title="Sales by Region",
                labels={'x': 'Region', 'y': 'Sales (₹)'},
                color=region_sales.values,
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


def render_geographic_analysis(data):
    """Render Geographic Analysis page."""
    st.title("🗺️ Geographic Analysis")
    st.markdown("Analyze performance across regions and states")
    
    geo_df = data['geographic_data'].copy()
    if geo_df.empty:
        st.warning("⚠️ Geographic data not available")
        return
    
    st.subheader("State-wise Performance")
    
    if 'state' in geo_df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            metric = st.selectbox(
                "Select Metric",
                ['revenue', 'customers', 'market_penetration', 'satisfaction'],
                key='geo_metric'
            )
        
        with col2:
            st.write("")
        
        if metric in geo_df.columns:
            geo_sorted = geo_df.sort_values(metric, ascending=True)
            
            fig = px.barh(
                x=geo_sorted[metric],
                y=geo_sorted['state'],
                title=f"{metric.replace('_', ' ').title()} by State",
                labels={'x': metric.replace('_', ' ').title(), 'y': 'State'},
                color=geo_sorted[metric],
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Detailed State Metrics")
    st.dataframe(geo_df, use_container_width=True)


def render_attribution_funnel(data):
    """Render Attribution & Funnel page."""
    st.title("🔗 Attribution & Funnel Analysis")
    st.markdown("Understand customer journey and channel attribution")
    
    tab1, tab2 = st.tabs(["Conversion Funnel", "Attribution Models"])
    
    with tab1:
        st.subheader("Marketing Conversion Funnel")
        funnel_df = data['funnel_data']
        if not funnel_df.empty and 'stage' in funnel_df.columns and 'visitors' in funnel_df.columns:
            funnel_sorted = funnel_df.sort_values('visitors', ascending=True)
            
            fig = px.bar(
                funnel_sorted,
                x='visitors',
                y='stage',
                orientation='h',
                title="Marketing Funnel - Visitor Journey",
                labels={'visitors': 'Visitors', 'stage': 'Stage'},
                color='visitors',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Funnel data not available")
    
    with tab2:
        st.subheader("Channel Attribution Models")
        attr_df = data['channel_attribution']
        if not attr_df.empty:
            st.dataframe(attr_df, use_container_width=True)
        else:
            st.info("ℹ️ Attribution data not available")


def render_ml_evaluation(data):
    """Render ML Model Evaluation page."""
    st.title("🤖 ML Model Evaluation")
    st.markdown("Analyze lead scoring model performance and insights")
    
    tab1, tab2, tab3 = st.tabs(["Model Performance", "Feature Importance", "Learning Curve"])
    
    with tab1:
        st.subheader("Lead Scoring Model Metrics")
        lead_df = data['lead_scoring_results']
        if not lead_df.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Predictions", len(lead_df))
            
            with col2:
                if 'predicted_class' in lead_df.columns:
                    positive = (lead_df['predicted_class'] == 1).sum()
                    st.metric("Predicted Converters", positive)
            
            with col3:
                if 'predicted_probability' in lead_df.columns:
                    avg_prob = lead_df['predicted_probability'].mean()
                    st.metric("Avg Confidence", f"{avg_prob:.2%}")
            
            st.dataframe(lead_df.head(10), use_container_width=True)
        else:
            st.info("ℹ️ Lead scoring data not available")
    
    with tab2:
        st.subheader("Feature Importance Analysis")
        feat_df = data['feature_importance']
        if not feat_df.empty and 'feature' in feat_df.columns and 'importance' in feat_df.columns:
            feat_sorted = feat_df.sort_values('importance', ascending=True)
            
            fig = px.barh(
                feat_sorted,
                x='importance',
                y='feature',
                title="Feature Importance Scores",
                labels={'importance': 'Importance Score', 'feature': 'Feature'},
                color='importance',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Feature importance data not available")
    
    with tab3:
        st.subheader("Learning Curve")
        learn_df = data['learning_curve']
        if not learn_df.empty:
            if 'training_set_size' in learn_df.columns and 'training_score' in learn_df.columns:
                fig = px.line(
                    learn_df,
                    x='training_set_size',
                    y=['training_score', 'validation_score'] if 'validation_score' in learn_df.columns else ['training_score'],
                    title="Learning Curve",
                    labels={'training_set_size': 'Training Set Size', 'value': 'Score'},
                    markers=True
                )
                fig.update_layout(height=400, hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.dataframe(learn_df, use_container_width=True)
        else:
            st.info("ℹ️ Learning curve data not available")


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
