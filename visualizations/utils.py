"""
Data processing utilities
"""

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc


def aggregate_by_channel(df, metric='revenue'):
    """Aggregate campaign data by channel."""
    if metric == 'revenue':
        return df.groupby('channel')['revenue'].sum().sort_values(ascending=False)
    elif metric == 'conversions':
        return df.groupby('channel')['conversions'].sum().sort_values(ascending=False)
    elif metric == 'roas':
        return (df.groupby('channel')['revenue'].sum() / df.groupby('channel')['spend'].sum()).sort_values(ascending=False)
    return df.groupby('channel')[metric].sum()


def aggregate_by_region_quarter(df):
    """Aggregate revenue by region and quarter."""
    df['date'] = pd.to_datetime(df['date'])
    df['quarter'] = df['date'].dt.quarter
    df['year'] = df['date'].dt.year
    return df.groupby(['region', 'quarter', 'year'])['revenue'].sum().reset_index()


def aggregate_daily_revenue(df):
    """Aggregate revenue by date."""
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby('date')['revenue'].sum().reset_index()


def aggregate_weekly_revenue(df):
    """Aggregate revenue by week."""
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.to_period('W'))['revenue'].sum().reset_index()


def aggregate_monthly_revenue(df):
    """Aggregate revenue by month."""
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.to_period('M'))['revenue'].sum().reset_index()


def calculate_cumulative_conversions(df):
    """Calculate cumulative conversions by channel over time."""
    df['date'] = pd.to_datetime(df['date'])
    result = df.groupby(['date', 'channel'])['conversions'].sum().reset_index()
    result = result.sort_values('date')
    result['cumulative_conversions'] = result.groupby('channel')['conversions'].cumsum()
    return result


def calculate_kpis(df):
    """Calculate key performance indicators."""
    total_revenue = df['revenue'].sum()
    total_conversions = df['conversions'].sum()
    total_spend = df['spend'].sum()
    roas = total_revenue / total_spend if total_spend > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'total_conversions': total_conversions,
        'total_spend': total_spend,
        'roas': roas,
        'avg_ctr': df['ctr'].mean() if 'ctr' in df.columns else 0,
        'avg_conversion_rate': (total_conversions / df['clicks'].sum() * 100) if 'clicks' in df.columns and df['clicks'].sum() > 0 else 0
    }


def calculate_confusion_matrix(y_true, y_pred):
    """Calculate confusion matrix metrics."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    return {
        'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp,
        'sensitivity': tp / (tp + fn) if (tp + fn) > 0 else 0,
        'specificity': tn / (tn + fp) if (tn + fp) > 0 else 0,
        'precision': tp / (tp + fp) if (tp + fp) > 0 else 0,
        'accuracy': (tp + tn) / (tp + tn + fp + fn)
    }


def calculate_roc_curve(y_true, y_prob):
    """Calculate ROC curve."""
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    
    return {
        'fpr': fpr,
        'tpr': tpr,
        'thresholds': thresholds,
        'auc': roc_auc
    }


def prepare_sunburst_data(df):
    """Prepare data for sunburst chart."""
    # Create hierarchy structure
    data = []
    
    # Root
    data.append({'label': 'All Customers', 'parent': '', 'value': len(df)})
    
    # By Region
    for region in df['region'].unique():
        region_df = df[df['region'] == region]
        data.append({'label': region, 'parent': 'All Customers', 'value': len(region_df)})
        
        # By Segment in Region
        for segment in region_df['segment'].unique():
            segment_df = region_df[region_df['segment'] == segment]
            data.append({
                'label': f"{segment} ({region})",
                'parent': region,
                'value': len(segment_df)
            })
    
    return pd.DataFrame(data)


def prepare_treemap_data(df):
    """Prepare product sales data for treemap."""
    data = []
    
    # Add root
    data.append({
        'label': 'All Products',
        'parent': '',
        'sales': df['sales'].sum(),
        'margin': df['margin'].mean()
    })
    
    # By Category
    for category in df['category'].unique():
        cat_df = df[df['category'] == category]
        data.append({
            'label': category,
            'parent': 'All Products',
            'sales': cat_df['sales'].sum(),
            'margin': cat_df['margin'].mean()
        })
        
        # By Subcategory
        for subcat in cat_df['subcategory'].unique():
            subcat_df = cat_df[cat_df['subcategory'] == subcat]
            data.append({
                'label': f"{subcat}",
                'parent': category,
                'sales': subcat_df['sales'].sum(),
                'margin': subcat_df['margin'].mean()
            })
    
    return pd.DataFrame(data)
