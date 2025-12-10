"""
Customer Insights Page
Distribution and relationship visualizations for customer data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from visualizations.charts import (
    create_histogram, create_box_plot, create_violin_plot,
    create_scatter_plot
)


def render(data):
    """Render the Customer Insights page."""
    
    st.title("👥 Customer Insights")
    st.markdown("Understand customer segments, demographics, and value distribution")
    
    customer_df = data['customer_data'].copy()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Demographics",
        "💰 Value Analysis",
        "😊 Satisfaction",
        "📈 Relationships"
    ])
    
    with tab1:
        st.subheader("Customer Age Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            bins = st.slider("Bin Width", 1, 20, 5, key="age_bins")
        
        with col2:
            segment_filter = st.multiselect(
                "Filter by Segment",
                customer_df['segment'].unique(),
                default=customer_df['segment'].unique(),
                key="seg_age"
            )
        
        filtered_df = customer_df[customer_df['segment'].isin(segment_filter)]
        
        fig = create_histogram(filtered_df, 'age', "Customer Age Distribution", bins=bins, height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: Customer base skews toward 25-40 age range. Different segments show distinct age profiles.")
    
    with tab2:
        st.subheader("Lifetime Value (LTV) by Customer Segment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            show_points = st.checkbox("Show individual data points", value=False, key="ltv_points")
        
        with col2:
            st.write("")
        
        fig = create_box_plot(
            customer_df,
            'segment',
            'ltv',
            "Lifetime Value by Segment",
            points=show_points,
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        st.subheader("Segment Statistics")
        segment_stats = customer_df.groupby('segment')['ltv'].agg([
            ('Mean LTV', 'mean'),
            ('Median LTV', 'median'),
            ('Min LTV', 'min'),
            ('Max LTV', 'max'),
            ('Customer Count', 'count')
        ]).round(2)
        
        st.dataframe(segment_stats, use_container_width=True)
        
        st.markdown("**Insight**: Premium segment shows highest median and widest spread. Churned customers have low LTV with some high-value lost customers (churn prevention opportunity).")
    
    with tab3:
        st.subheader("Satisfaction Score Distribution by NPS Category")
        
        col1, col2 = st.columns(2)
        
        with col1:
            split_by = st.selectbox(
                "Split by",
                ["None", "Channel", "Region"],
                key="satisfaction_split"
            )
        
        with col2:
            st.write("")
        
        if split_by == "None":
            fig = create_violin_plot(
                customer_df,
                'nps_category',
                'satisfaction_score',
                "Satisfaction Distribution by NPS Category",
                height=450
            )
        else:
            fig = px.violin(
                customer_df,
                x='nps_category',
                y='satisfaction_score',
                color=split_by.lower(),
                title=f"Satisfaction Distribution by NPS Category (split by {split_by})",
                points="outliers"
            )
            fig.update_layout(height=450)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: Clear separation between NPS groups. Detractors show bimodal distribution suggesting two distinct dissatisfaction drivers.")
    
    with tab4:
        st.subheader("Customer Value Relationships")
        
        col1, col2 = st.columns(2)
        
        with col1:
            show_trendline = st.checkbox("Show trend line", value=False, key="income_trend")
        
        with col2:
            st.write("")
        
        fig = create_scatter_plot(
            customer_df,
            'income',
            'ltv',
            'segment',
            title="Income vs. Lifetime Value by Segment",
            height=450,
            trendline=show_trendline
        )
        fig.update_layout(
            xaxis_title="Income (₹)",
            yaxis_title="Lifetime Value (₹)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: Positive correlation between income and LTV. Premium customers cluster in high-income/high-LTV quadrant. Some Budget customers show high LTV (upgrade potential).")
        
        # Additional scatter: Purchases vs Satisfaction
        st.subheader("Purchase Frequency vs. Satisfaction")
        
        fig2 = px.scatter(
            customer_df,
            x='purchases',
            y='satisfaction_score',
            color='segment',
            size='ltv',
            hover_name='segment',
            title="Purchase Frequency vs. Satisfaction Score",
            labels={
                'purchases': 'Number of Purchases',
                'satisfaction_score': 'Satisfaction Score (1-10)'
            }
        )
        fig2.update_layout(height=450)
        st.plotly_chart(fig2, use_container_width=True)
