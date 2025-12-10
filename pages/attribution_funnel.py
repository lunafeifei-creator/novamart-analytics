"""
Attribution & Funnel Analysis Page
Conversion funnel and attribution model comparison
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def render(data):
    """Render the Attribution & Funnel page."""
    
    st.title("🔗 Attribution & Funnel Analysis")
    st.markdown("Understand customer journey and channel attribution")
    
    funnel_df = data['funnel_data'].copy()
    channel_attr_df = data['channel_attribution']
    corr_df = data['correlation_matrix'].copy()
    
    tab1, tab2, tab3 = st.tabs([
        "📊 Conversion Funnel",
        "🔀 Attribution Models",
        "🔗 Metric Correlations"
    ])
    
    with tab1:
        st.subheader("Marketing Conversion Funnel")
        
        # Ensure stage order
        stage_order = ['Awareness', 'Interest', 'Consideration', 'Evaluation', 'Purchase']
        funnel_df['stage'] = pd.Categorical(funnel_df['stage'], categories=stage_order, ordered=True)
        funnel_df = funnel_df.sort_values('stage')
        
        # Create funnel chart
        fig = go.Figure(go.Funnel(
            x=funnel_df['stage'].values,
            y=funnel_df['visitors'].values,
            marker=dict(
                color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            ),
            textposition='inside',
            textinfo='value+percent parent'
        ))
        
        fig.update_layout(
            title="Visitor Journey Through Marketing Funnel",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Funnel metrics
        st.subheader("Funnel Analysis")
        
        funnel_metrics = []
        for i in range(len(funnel_df) - 1):
            current_stage = funnel_df.iloc[i]
            next_stage = funnel_df.iloc[i + 1]
            
            conversion_rate = (next_stage['visitors'] / current_stage['visitors'] * 100) if current_stage['visitors'] > 0 else 0
            drop_off = current_stage['visitors'] - next_stage['visitors']
            
            funnel_metrics.append({
                'Stage Transition': f"{current_stage['stage']} → {next_stage['stage']}",
                'Conversion Rate': f"{conversion_rate:.1f}%",
                'Drop-off': f"{drop_off:,}",
                'Remaining': f"{next_stage['visitors']:,}"
            })
        
        metrics_df = pd.DataFrame(funnel_metrics)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Key Insights**:
        - **Biggest Drop-off**: Awareness → Interest (55% loss) - Focus on improving top-of-funnel engagement
        - **Strong Bottom Funnel**: Evaluation → Purchase (53% conversion) - Sales process is effective
        - **Optimization Opportunity**: Mid-funnel (Interest & Consideration) shows room for improvement
        """)
    
    with tab2:
        st.subheader("Attribution Model Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_model = st.selectbox(
                "Select Attribution Model",
                channel_attr_df.columns[1:],  # Exclude channel column
                key="attr_model"
            )
        
        with col2:
            st.write("")
        
        # Prepare data for selected model
        model_data = channel_attr_df[['channel', selected_model]].copy()
        model_data = model_data.sort_values(selected_model, ascending=True)
        
        # Create pie/donut chart
        fig = px.pie(
            model_data,
            values=selected_model,
            names='channel',
            title=f"Channel Attribution - {selected_model} Model",
            hole=0.4,
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparison table
        st.subheader("All Attribution Models")
        
        attr_display = channel_attr_df.copy()
        attr_display.columns = ['Channel'] + list(attr_display.columns[1:])
        
        st.dataframe(attr_display, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Attribution Model Insights**:
        - **First-Touch**: Credits initial awareness channel (e.g., Google Ads)
        - **Last-Touch**: Credits final conversion channel (e.g., Email)
        - **Linear**: Distributes credit equally across all touchpoints
        - **Time-Decay**: Gives more credit to touchpoints closer to conversion
        - **Position-Based**: Credits first and last touchpoints, 40% each
        """)
    
    with tab3:
        st.subheader("Marketing Metrics Correlation Matrix")
        
        # Set index if needed
        if corr_df.index.name != 'Metric':
            corr_df = corr_df.set_index(corr_df.columns[0])
        
        # Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_df.values,
            x=corr_df.columns,
            y=corr_df.index,
            colorscale='RdBu_r',
            zmid=0,
            text=np.round(corr_df.values, 2),
            texttemplate='%{text:.2f}',
            textfont={"size": 9},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Correlation Matrix - Marketing Metrics",
            height=600,
            width=800
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Key Correlations**:
        - **Strong Positive**: Spend-Impressions-Clicks (expected scaling relationships)
        - **Negative Correlation**: ROAS vs. Spend (suggests diminishing returns at higher spend levels)
        - **Cart Abandonment**: Negatively correlates with Conversions (optimization area)
        """)
