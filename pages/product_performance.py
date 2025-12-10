"""
Product Performance Page
Product sales hierarchy and performance analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render(data):
    """Render the Product Performance page."""
    
    st.title("🛍️ Product Performance")
    st.markdown("Analyze product sales hierarchy and profitability")
    
    product_df = data['product_sales'].copy()
    
    tab1, tab2, tab3 = st.tabs([
        "🗂️ Product Hierarchy",
        "📊 Category Performance",
        "🌍 Regional Analysis"
    ])
    
    with tab1:
        st.subheader("Product Sales Hierarchy (Treemap)")
        
        # Prepare treemap data
        treemap_data = []
        
        # Add root
        treemap_data.append({
            'label': 'All Products',
            'parent': '',
            'sales': product_df['sales'].sum(),
            'margin': 0
        })
        
        # By Category
        for category in product_df['category'].unique():
            cat_df = product_df[product_df['category'] == category]
            treemap_data.append({
                'label': category,
                'parent': 'All Products',
                'sales': cat_df['sales'].sum(),
                'margin': cat_df['profit_margin'].mean()
            })
            
            # By Subcategory
            for subcat in cat_df['subcategory'].unique():
                subcat_df = cat_df[cat_df['subcategory'] == subcat]
                treemap_data.append({
                    'label': subcat,
                    'parent': category,
                    'sales': subcat_df['sales'].sum(),
                    'margin': subcat_df['profit_margin'].mean()
                })
        
        treemap_df = pd.DataFrame(treemap_data)
        
        fig = go.Figure(go.Treemap(
            labels=treemap_df['label'],
            parents=treemap_df['parent'],
            values=treemap_df['sales'],
            marker=dict(
                colors=treemap_df['margin'],
                colorscale='Viridis',
                cmid=treemap_df['margin'].median(),
                showscale=True,
                colorbar=dict(title="Profit<br>Margin %")
            ),
            text=[f"₹{x/1000:.0f}K" if x >= 1000 else f"₹{x:.0f}" for x in treemap_df['sales']],
            textposition='middle center',
            hovertemplate='<b>%{label}</b><br>Sales: ₹%{value}<br>Margin: %{color:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="Product Sales Hierarchy (Size = Sales, Color = Profit Margin)",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Insight**: Electronics dominates sales volume. Fashion has highest margins (darker color). Identify high-volume low-margin products for pricing review.")
    
    with tab2:
        st.subheader("Category Performance Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            metric = st.selectbox(
                "Select Metric",
                ["Sales", "Profit Margin", "Units Sold"],
                key="prod_metric"
            )
        
        with col2:
            st.write("")
        
        # Category aggregation
        if metric == "Sales":
            cat_perf = product_df.groupby('category')['sales'].sum().sort_values(ascending=True)
            title = "Total Sales by Category"
        elif metric == "Profit Margin":
            cat_perf = product_df.groupby('category')['profit_margin'].mean().sort_values(ascending=True)
            title = "Average Profit Margin by Category"
        else:
            cat_perf = product_df.groupby('category')['units'].sum().sort_values(ascending=True)
            title = "Units Sold by Category"
        
        fig = px.barh(
            x=cat_perf.values,
            y=cat_perf.index,
            title=title,
            labels={'x': metric, 'y': 'Category'},
            color=cat_perf.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("Category Details")
        category_stats = product_df.groupby('category').agg({
            'sales': ['sum', 'mean'],
            'units': 'sum',
            'profit_margin': 'mean'
        }).round(2)
        
        category_stats.columns = ['Total Sales', 'Avg Sale', 'Units Sold', 'Avg Margin %']
        st.dataframe(category_stats, use_container_width=True)
    
    with tab3:
        st.subheader("Regional Product Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_category = st.selectbox(
                "Select Category",
                product_df['category'].unique(),
                key="prod_region"
            )
        
        with col2:
            selected_metric = st.selectbox(
                "Select Metric",
                ["Sales", "Units", "Margin"],
                key="prod_region_metric"
            )
        
        # Filter data
        cat_filter_df = product_df[product_df['category'] == selected_category]
        
        if selected_metric == "Sales":
            region_perf = cat_filter_df.groupby('region')['sales'].sum().sort_values(ascending=False)
            metric_label = "Sales (₹)"
        elif selected_metric == "Units":
            region_perf = cat_filter_df.groupby('region')['units'].sum().sort_values(ascending=False)
            metric_label = "Units Sold"
        else:
            region_perf = cat_filter_df.groupby('region')['profit_margin'].mean().sort_values(ascending=False)
            metric_label = "Profit Margin %"
        
        fig = px.bar(
            x=region_perf.index,
            y=region_perf.values,
            title=f"{selected_category} - {selected_metric} by Region",
            labels={'x': 'Region', 'y': metric_label},
            color=region_perf.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Quarterly trend
        st.subheader(f"Quarterly Trend - {selected_category}")
        
        quarterly_perf = cat_filter_df.groupby('quarter')['sales'].sum().reset_index()
        quarterly_perf = quarterly_perf.sort_values('quarter')
        
        fig2 = px.line(
            quarterly_perf,
            x='quarter',
            y='sales',
            title=f"Quarterly Sales Trend - {selected_category}",
            markers=True,
            labels={'quarter': 'Quarter', 'sales': 'Sales (₹)'}
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
