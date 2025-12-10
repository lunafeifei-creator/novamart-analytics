"""
Geographic Analysis Page
State-level and location-based performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render(data):
    """Render the Geographic Analysis page."""
    
    st.title("🗺️ Geographic Analysis")
    st.markdown("Analyze performance across Indian states and regions")
    
    geo_df = data['geographic_data'].copy()
    
    tab1, tab2, tab3 = st.tabs([
        "🗺️ State Performance Map",
        "📊 Detailed Metrics",
        "📈 Growth Analysis"
    ])
    
    with tab1:
        st.subheader("State-wise Performance")
        
        metric = st.selectbox(
            "Select Metric to Visualize",
            ["Revenue", "Customers", "Market Penetration", "Satisfaction"],
            key="geo_metric"
        )
        
        if metric == "Revenue":
            metric_col = 'revenue'
            scale = 'Blues'
            title = "Revenue by State"
        elif metric == "Customers":
            metric_col = 'customers'
            scale = 'Greens'
            title = "Customer Count by State"
        elif metric == "Market Penetration":
            metric_col = 'market_penetration'
            scale = 'Oranges'
            title = "Market Penetration % by State"
        else:
            metric_col = 'satisfaction'
            scale = 'Reds'
            title = "Average Satisfaction by State"
        
        # Create bar chart (since we don't have actual geo data, use bar)
        geo_sorted = geo_df.sort_values(metric_col, ascending=True)
        
        fig = px.barh(
            geo_sorted,
            x=metric_col,
            y='state',
            title=title,
            color=metric_col,
            color_continuous_scale=scale,
            labels={metric_col: metric}
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"**Insight**: Top performers identified. Maharashtra and Karnataka are strong markets. Eastern states show growth potential.")
    
    with tab2:
        st.subheader("Detailed State Metrics")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                ["Revenue", "Customers", "Satisfaction"],
                key="sort_metric"
            )
        
        with col2:
            sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True, key="sort_order")
        
        # Prepare display data
        display_df = geo_df[[
            'state', 'revenue', 'customers', 'market_penetration', 'satisfaction'
        ]].copy()
        
        display_df.columns = ['State', 'Revenue (₹)', 'Customers', 'Market Penetration %', 'Satisfaction']
        
        if sort_by == "Revenue":
            display_df = display_df.sort_values('Revenue (₹)', ascending=(sort_order == "Ascending"))
        elif sort_by == "Customers":
            display_df = display_df.sort_values('Customers', ascending=(sort_order == "Ascending"))
        else:
            display_df = display_df.sort_values('Satisfaction', ascending=(sort_order == "Ascending"))
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Statistics
        st.subheader("Overall Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Revenue", f"₹{geo_df['revenue'].sum():,.0f}")
        
        with col2:
            st.metric("Total Customers", f"{geo_df['customers'].sum():,}")
        
        with col3:
            st.metric("Avg Penetration", f"{geo_df['market_penetration'].mean():.1f}%")
        
        with col4:
            st.metric("Avg Satisfaction", f"{geo_df['satisfaction'].mean():.1f}/10")
    
    with tab3:
        st.subheader("Growth & Potential Analysis")
        
        # Sort states by growth potential
        growth_analysis = geo_df[[
            'state', 'customers', 'market_penetration', 'satisfaction', 'revenue'
        ]].copy()
        
        # Calculate opportunity score (high growth potential = low penetration + high satisfaction + reasonable customer base)
        growth_analysis['opportunity_score'] = (
            (100 - growth_analysis['market_penetration']) * 0.4 +  # Lower penetration = higher opportunity
            growth_analysis['satisfaction'] * 0.4 +  # Higher satisfaction = better execution
            (growth_analysis['customers'] / growth_analysis['customers'].max() * 100) * 0.2  # Market size
        )
        
        growth_analysis = growth_analysis.sort_values('opportunity_score', ascending=True)
        
        fig = px.barh(
            growth_analysis,
            x='opportunity_score',
            y='state',
            title="Growth Opportunity Score by State",
            color='opportunity_score',
            color_continuous_scale='Viridis',
            labels={'opportunity_score': 'Opportunity Score'}
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Opportunity Score Calculation**:
        - **40% - Market Penetration**: Lower penetration = higher growth potential
        - **40% - Customer Satisfaction**: Higher satisfaction = better execution capability
        - **20% - Market Size**: Larger customer base = more growth volume
        
        **Strategy**: Focus on states with high opportunity scores for expansion.
        """)
        
        # Top opportunities
        st.subheader("Top 5 Growth Opportunities")
        top_opportunities = growth_analysis.tail(5)[['state', 'customers', 'market_penetration', 'satisfaction', 'opportunity_score']].copy()
        top_opportunities.columns = ['State', 'Current Customers', 'Penetration %', 'Satisfaction', 'Opportunity Score']
        
        st.dataframe(top_opportunities, use_container_width=True, hide_index=True)
