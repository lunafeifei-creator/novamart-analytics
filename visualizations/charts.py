"""
Visualization utilities and chart functions
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import altair as alt
from config import CHANNEL_COLORS, SEGMENT_COLORS
import streamlit as st


def create_bar_chart(data, x, y, title, color=None, orientation='v', height=400):
    """Create a bar chart with Plotly."""
    fig = px.bar(
        data, 
        x=x if orientation == 'v' else y, 
        y=y if orientation == 'v' else x,
        color=color,
        title=title,
        color_discrete_map=CHANNEL_COLORS if color == 'channel' else None,
        barmode='group'
    )
    fig.update_layout(height=height, hovermode='x unified')
    return fig


def create_line_chart(data, x, y, title, color=None, height=400):
    """Create a line chart with Plotly."""
    fig = px.line(
        data, 
        x=x, 
        y=y,
        color=color,
        title=title,
        markers=True
    )
    fig.update_layout(height=height, hovermode='x unified')
    return fig


def create_area_chart(data, x, y, title, color=None, height=400):
    """Create an area chart with Plotly."""
    fig = px.area(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        groupnorm='percent'
    )
    fig.update_layout(height=height, hovermode='x unified')
    return fig


def create_scatter_plot(data, x, y, color, size=None, title="", height=400, trendline=False):
    """Create a scatter plot with optional trendline."""
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        size=size,
        title=title,
        trendline="ols" if trendline else None,
        color_discrete_map=SEGMENT_COLORS
    )
    fig.update_layout(height=height, hovermode='closest')
    return fig


def create_box_plot(data, x, y, title="", height=400, points=False):
    """Create a box plot."""
    fig = px.box(
        data,
        x=x,
        y=y,
        title=title,
        points="all" if points else None
    )
    fig.update_layout(height=height)
    return fig


def create_violin_plot(data, x, y, title="", height=400):
    """Create a violin plot."""
    fig = px.violin(
        data,
        x=x,
        y=y,
        title=title,
        points="outliers"
    )
    fig.update_layout(height=height)
    return fig


def create_histogram(data, x, title="", bins=30, height=400):
    """Create a histogram."""
    fig = px.histogram(
        data,
        x=x,
        title=title,
        nbins=bins
    )
    fig.update_layout(height=height)
    return fig


def create_heatmap(data, title="", height=500):
    """Create a heatmap from correlation matrix."""
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='RdBu_r',
        zmid=0,
        text=np.round(data.values, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    fig.update_layout(title=title, height=height)
    return fig


def create_funnel_chart(data, x, y, title="", height=400):
    """Create a funnel chart."""
    fig = go.Figure(go.Funnel(
        x=data[x].values,
        y=data[y].values,
        marker=dict(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ))
    fig.update_layout(title=title, height=height)
    return fig


def create_sunburst(data, labels, parents, values, title="", height=500):
    """Create a sunburst chart."""
    fig = go.Figure(go.Sunburst(
        labels=data[labels].values,
        parents=data[parents].values,
        values=data[values].values,
        marker=dict(
            colorscale='Blues',
            cmid=2
        )
    ))
    fig.update_layout(title=title, height=height)
    return fig


def create_treemap(data, labels, parents, values, color=None, title="", height=500):
    """Create a treemap."""
    fig = go.Figure(go.Treemap(
        labels=data[labels].values,
        parents=data[parents].values,
        values=data[values].values,
        marker=dict(
            colors=data[color].values if color else None,
            colorscale='Viridis',
            showscale=True if color else False
        )
    ))
    fig.update_layout(title=title, height=height)
    return fig


def create_metric_card(label, value, delta=None, delta_color="normal"):
    """Create a styled metric card with Streamlit."""
    col = st.container()
    with col:
        st.metric(label, value, delta=delta, delta_color=delta_color)


def create_altair_heatmap(data, x, y, color, title="", height=400, width=600):
    """Create a heatmap using Altair."""
    chart = alt.Chart(data).mark_rect().encode(
        x=alt.X(x, axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(y),
        color=alt.Color(color, scale=alt.Scale(scheme='blues')),
        tooltip=[x, y, color]
    ).properties(
        width=width,
        height=height,
        title=title
    ).interactive()
    
    return chart
