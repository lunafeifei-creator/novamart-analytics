"""
ML Model Evaluation Page
Confusion matrix, ROC curve, learning curve, and feature importance
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, roc_curve, auc


def render(data):
    """Render the ML Model Evaluation page."""
    
    st.title("🤖 ML Model Evaluation")
    st.markdown("Analyze lead scoring model performance and feature importance")
    
    lead_scoring_df = data['lead_scoring_results'].copy()
    feature_importance_df = data['feature_importance'].copy()
    learning_curve_df = data['learning_curve'].copy()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Confusion Matrix",
        "📈 ROC Curve",
        "📉 Learning Curve",
        "⭐ Feature Importance"
    ])
    
    with tab1:
        st.subheader("Lead Scoring Model - Confusion Matrix")
        
        # Calculate confusion matrix
        cm = confusion_matrix(
            lead_scoring_df['actual_converted'],
            lead_scoring_df['predicted_class']
        )
        
        tn, fp, fn, tp = cm.ravel()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicted No', 'Predicted Yes'],
            y=['Actual No', 'Actual Yes'],
            text=cm,
            texttemplate='%{text}',
            textfont={"size": 16},
            colorscale='Blues',
            showscale=False
        ))
        
        fig.update_layout(
            title="Confusion Matrix - Lead Scoring Model",
            xaxis_title="Predicted",
            yaxis_title="Actual",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        
        with col1:
            st.metric("Sensitivity (Recall)", f"{sensitivity:.1%}")
        
        with col2:
            st.metric("Specificity", f"{specificity:.1%}")
        
        with col3:
            st.metric("Precision", f"{precision:.1%}")
        
        with col4:
            st.metric("Accuracy", f"{accuracy:.1%}")
        
        st.markdown(f"""
        **Interpretation**:
        - **True Positives (TP)**: {tp} - Leads correctly identified as converters
        - **False Positives (FP)**: {fp} - Non-converters incorrectly marked as converters (acceptable for lead gen)
        - **True Negatives (TN)**: {tn} - Non-converters correctly identified
        - **False Negatives (FN)**: {fn} - Converters missed (opportunity cost)
        
        **Insight**: Model shows good true positive rate. False negatives should be minimized to avoid missing conversion opportunities.
        """)
    
    with tab2:
        st.subheader("ROC Curve - Model Discrimination")
        
        # Calculate ROC curve
        fpr, tpr, thresholds = roc_curve(
            lead_scoring_df['actual_converted'],
            lead_scoring_df['predicted_probability']
        )
        
        roc_auc = auc(fpr, tpr)
        
        # Find optimal threshold (Youden's J statistic)
        optimal_idx = np.argmax(tpr - fpr)
        optimal_threshold = thresholds[optimal_idx]
        
        # Create ROC curve plot
        fig = go.Figure()
        
        # ROC Curve
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f'ROC Curve (AUC = {roc_auc:.3f})',
            line=dict(color='#1f77b4', width=3)
        ))
        
        # Diagonal (random classifier)
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(color='gray', dash='dash')
        ))
        
        # Optimal point
        fig.add_trace(go.Scatter(
            x=[fpr[optimal_idx]], y=[tpr[optimal_idx]],
            mode='markers',
            name=f'Optimal Threshold ({optimal_threshold:.3f})',
            marker=dict(size=12, color='red')
        ))
        
        fig.update_layout(
            title="ROC Curve - Lead Scoring Model",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("AUC Score", f"{roc_auc:.3f}")
        
        with col2:
            st.metric("Optimal Threshold", f"{optimal_threshold:.3f}")
        
        with col3:
            threshold_quality = "Excellent" if roc_auc > 0.8 else "Good" if roc_auc > 0.7 else "Fair"
            st.metric("Model Quality", threshold_quality)
        
        st.markdown(f"""
        **Insight**: 
        - AUC of {roc_auc:.3f} indicates {'excellent' if roc_auc > 0.8 else 'good'} model discrimination
        - Curve stays well above diagonal (much better than random)
        - Optimal threshold around {optimal_threshold:.3f} balances sensitivity and specificity
        """)
    
    with tab3:
        st.subheader("Learning Curve - Model Diagnostics")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write("")
        
        with col2:
            show_bands = st.checkbox("Show confidence bands", value=True, key="learning_bands")
        
        # Prepare learning curve data
        lc_data = learning_curve_df.copy()
        
        fig = go.Figure()
        
        # Training curve
        fig.add_trace(go.Scatter(
            x=lc_data['training_set_size'],
            y=lc_data['training_score'],
            mode='lines+markers',
            name='Training Score',
            line=dict(color='#1f77b4')
        ))
        
        # Validation curve
        fig.add_trace(go.Scatter(
            x=lc_data['training_set_size'],
            y=lc_data['validation_score'],
            mode='lines+markers',
            name='Validation Score',
            line=dict(color='#ff7f0e')
        ))
        
        if show_bands and 'training_std' in lc_data.columns:
            # Training confidence band
            fig.add_trace(go.Scatter(
                x=lc_data['training_set_size'].tolist() + lc_data['training_set_size'].tolist()[::-1],
                y=(lc_data['training_score'] + lc_data['training_std']).tolist() +
                  (lc_data['training_score'] - lc_data['training_std']).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(31, 119, 180, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False,
                name='Training Band'
            ))
            
            # Validation confidence band
            fig.add_trace(go.Scatter(
                x=lc_data['training_set_size'].tolist() + lc_data['training_set_size'].tolist()[::-1],
                y=(lc_data['validation_score'] + lc_data['validation_std']).tolist() +
                  (lc_data['validation_score'] - lc_data['validation_std']).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255, 127, 14, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False,
                name='Validation Band'
            ))
        
        fig.update_layout(
            title="Learning Curve - Training vs Validation",
            xaxis_title="Training Set Size",
            yaxis_title="Model Score",
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Interpretation**:
        - **Converging Curves**: Indicates no overfitting (good generalization)
        - **Gap Between Curves**: Small gap suggests model is not underfitting
        - **Trend**: Curves plateau suggests diminishing returns from more data
        
        **Recommendation**: Model is well-balanced. Continue monitoring with new data.
        """)
    
    with tab4:
        st.subheader("Feature Importance - Model Interpretability")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sort_direction = st.radio("Sort Direction", ["Descending", "Ascending"], horizontal=True, key="feat_sort")
        
        with col2:
            show_errors = st.checkbox("Show error bars", value=True, key="feat_errors")
        
        # Prepare feature importance data
        fi_data = feature_importance_df.copy()
        fi_data = fi_data.sort_values('importance', ascending=(sort_direction == "Ascending"))
        
        # Create bar chart
        fig = px.bar(
            fi_data,
            y='feature',
            x='importance',
            orientation='h',
            title="Feature Importance - Lead Scoring Model",
            labels={'feature': 'Feature', 'importance': 'Importance Score'},
            color='importance',
            color_continuous_scale='Viridis'
        )
        
        if show_errors and 'std_dev' in fi_data.columns:
            fig.add_traces(go.Bar(
                y=fi_data['feature'],
                x=fi_data['importance'],
                error_x=dict(
                    type='data',
                    array=fi_data['std_dev'],
                    visible=True
                ),
                showlegend=False,
                marker_color='rgba(0,0,0,0)',
                hoverinfo='skip'
            ))
        
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top features insights
        st.subheader("Feature Insights")
        
        top_3 = fi_data.head(3)
        col1, col2, col3 = st.columns(3)
        
        for idx, (col, row) in enumerate(zip([col1, col2, col3], top_3.itertuples())):
            with col:
                st.info(f"""
                **{idx+1}. {row.feature}**
                
                Importance: {row.importance:.3f}
                """)
        
        st.markdown("""
        **Key Insights**:
        - **Webinar Attendance** and **Form Submissions** are strongest predictors
        - **Email Opens** alone have low predictive value (requires other signals)
        - **Business Implication**: Invest more in webinars for lead quality improvement
        """)
