# NovaMart Marketing Analytics Dashboard

An interactive Streamlit dashboard for comprehensive marketing analytics and business intelligence for NovaMart, a multi-channel retail company.

## 📊 Overview

This dashboard provides data-driven insights across marketing campaigns, customer behavior, product performance, and machine learning model evaluation. Built with Python and Streamlit, it enables real-time exploration of marketing performance metrics across multiple dimensions.

## ✨ Features

### 📊 Executive Overview
- Key Performance Indicators (KPIs): Revenue, Conversions, ROAS, Customer Count
- Revenue trend analysis with multiple time aggregation options
- Channel performance comparison

### 📈 Campaign Analytics
- Revenue trends over time (daily/weekly/monthly)
- Regional performance analysis by quarter
- Campaign type budget allocation and spending patterns
- Daily performance calendar heatmap

### 👥 Customer Insights
- Customer age distribution with customizable histogram bins
- Lifetime Value (LTV) analysis by customer segment
- Satisfaction score distribution by NPS category
- Customer relationship analysis (income vs. LTV)

### 🛍️ Product Performance
- Interactive product sales hierarchy (treemap visualization)
- Category performance metrics
- Regional product performance analysis
- Quarterly sales trends

### 🗺️ Geographic Analysis
- Interactive geographic map showing state-wise performance (latitude/longitude visualization)
- Selectable metrics for map visualization
- State-wise revenue and customer distribution
- Market penetration and satisfaction metrics
- Detailed state metrics table

### 🔗 Attribution & Funnel
- Marketing funnel visualization with conversion rates
- Multi-touch attribution model comparison (first-touch, last-touch, linear, time-decay, position-based)
- Correlation matrix heatmap for marketing metrics

### 🤖 ML Model Evaluation
- Confusion matrix visualization for lead scoring model
- ROC curve analysis with optimal threshold identification
- Learning curve diagnostics
- Feature importance analysis with error bars

## 📁 Project Structure

```
novamart-analytics/
├── app.py                          # Main application entry point (single-file architecture)
├── config.py                       # Configuration and color schemes
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .streamlit/
│   ├── config.toml                # Streamlit configuration
│   └── secrets.toml.example        # Example secrets file
├── .gitignore                      # Git ignore rules
├── data/                           # CSV datasets
│   ├── campaign_performance.csv
│   ├── customer_data.csv
│   ├── product_sales.csv
│   ├── lead_scoring_results.csv
│   ├── feature_importance.csv
│   ├── learning_curve.csv
│   ├── geographic_data.csv
│   ├── channel_attribution.csv
│   ├── funnel_data.csv
│   ├── customer_journey.csv
│   └── correlation_matrix.csv
└── visualizations/                 # Visualization utilities
    ├── __init__.py
    ├── charts.py                   # Chart creation functions
    └── utils.py                    # Data processing utilities
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/novamart-analytics.git
cd novamart-analytics
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Ensure CSV datasets** are placed in the `data/` subdirectory (they should already be there)

5. **Run the application**
```bash
streamlit run app.py
```

6. **Access the dashboard**
Open your browser and navigate to `http://localhost:8501`

## 📊 Data Requirements

The dashboard expects the following CSV files in the project root:

| File | Records | Key Metrics |
|------|---------|-------------|
| `campaign_performance.csv` | 5,858 | Impressions, Clicks, Conversions, Spend, Revenue, CTR, CPA, ROAS |
| `customer_data.csv` | 5,000 | Age, Income, LTV, Purchases, Satisfaction, Churn Status |
| `product_sales.csv` | 1,440 | Category, Sales, Units, Profit Margin |
| `lead_scoring_results.csv` | 2,000 | Predictions, Probabilities, Conversion Status |
| `feature_importance.csv` | Variable | Feature Names, Importance Scores, Std Dev |
| `learning_curve.csv` | Variable | Training Size, Training Score, Validation Score |
| `geographic_data.csv` | 17 | State, Region, Latitude, Longitude, Total Customers, Total Revenue, Market Penetration, Customer Satisfaction |
| `channel_attribution.csv` | 8+ | Channel Names, Attribution Model Percentages |
| `funnel_data.csv` | 5+ | Stage, Visitor Count, Conversion Rate |
| `customer_journey.csv` | Variable | Touchpoint Flows |
| `correlation_matrix.csv` | 10x10 | Metric Correlations |

## 🔧 Configuration

Edit `config.py` to customize:
- Page configuration and layout
- Color schemes and palettes
- Channel and segment colors
- Chart defaults

```python
# Example: Add custom color for new channel
CHANNEL_COLORS = {
    "Google Ads": "#4285F4",
    "Your Channel": "#YOUR_HEX_COLOR",
    ...
}
```

## 📈 Key Features Explained

### Interactive Filters
- Date range selectors for temporal analysis
- Dropdown and multi-select filters for drilling down
- Toggle switches for view mode changes

### Responsive Design
- Automatically adapts to different screen sizes
- Wide layout optimized for monitoring dashboards
- Column-based layout for organized content

### Performance Optimization
- Caching with `@st.cache_data` for fast data loading
- Vectorized pandas operations
- Lazy loading of visualizations

## 🌐 Deployment to Streamlit Cloud

### Prerequisites
- GitHub account with repository containing the code
- Streamlit Cloud account (free at streamlit.io)

### Deployment Steps

1. **Prepare your GitHub repository**
```bash
git init
git add .
git commit -m "Initial commit: NovaMart Analytics Dashboard"
git push origin main
```

2. **Deploy to Streamlit Cloud**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select repository, branch, and main file (`app.py`)
   - Click "Deploy"

3. **Configure secrets (if needed)**
   - Create `.streamlit/secrets.toml` for sensitive data
   - Use `st.secrets` to access them in the app

### Example `.streamlit/secrets.toml`
```toml
# Add any API keys or sensitive configuration here
db_username = "user"
db_password = "password"
```

## 📚 Libraries Used

- **Streamlit**: Interactive web app framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Altair**: Declarative visualization
- **Scikit-learn**: ML model evaluation and metrics
- **Numpy**: Numerical computing

## 🎯 Key Insights Generated

The dashboard helps stakeholders discover:

1. **Channel Performance**: Which marketing channels drive highest revenue and conversion quality
2. **Geographic Opportunities**: Regions with growth potential based on penetration and satisfaction
3. **Customer Segmentation**: LTV distribution and upgrade opportunities
4. **Product Strategy**: High-margin products and low-margin optimization opportunities
5. **Funnel Optimization**: Stages with highest drop-off and improvement potential
6. **ML Model Quality**: Lead scoring model reliability and feature importance

## 🔍 Troubleshooting

### Common Issues

**"ModuleNotFoundError"**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Or install specific package
pip install streamlit==1.28.1
```

**"FileNotFoundError: CSV file not found"**
- Check that all CSV files are in the project root directory
- Verify file names match exactly (case-sensitive)
- Update file paths in `app.py` if needed

**"Slow dashboard loading"**
- Clear Streamlit cache: `streamlit cache clear`
- Reduce data size or use data sampling
- Check for expensive computations in visualization functions

**"Charts not displaying"**
- Verify data format matches expected columns
- Check for null/missing values in critical columns
- Review browser console for JavaScript errors

## 📝 Development Guide

### Adding a New Visualization

1. Create a function in `visualizations/charts.py`:
```python
def create_custom_chart(data, x_col, y_col, title):
    fig = px.your_chart_type(data, x=x_col, y=y_col, title=title)
    return fig
```

2. Use it in a page module:
```python
from visualizations.charts import create_custom_chart

fig = create_custom_chart(df, 'x_column', 'y_column', 'Title')
st.plotly_chart(fig, use_container_width=True)
```

### Adding a New Page

1. Create a new `render_<page_name>(data)` function in `app.py`
2. Implement your visualizations and content in the function
3. Add the function to the `pages` dictionary in the `main()` function:
```python
pages = {
    "📊 Executive Overview": render_executive_overview,
    "📈 Campaign Analytics": render_campaign_analytics,
    # Add your new page here:
    "📌 Your New Page": render_your_page,
}
```
4. The page will automatically appear in the sidebar navigation radio button menu

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**Your Name/Organization**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- NovaMart team for the business context and requirements
- Streamlit community for excellent documentation
- Plotly for interactive visualization capabilities

## 📞 Support

For issues, questions, or suggestions:
- Open an GitHub Issue
- Check existing issues for solutions
- Review Streamlit documentation at https://docs.streamlit.io

## 🗺️ Roadmap

- [ ] Real-time data integration with databases
- [ ] Predictive analytics and forecasting
- [ ] Advanced segmentation and cohort analysis
- [ ] Custom report generation and export
- [ ] User authentication and role-based access
- [ ] Dark mode theme support
- [ ] Multi-language support

---

**Last Updated**: December 2024
**Version**: 1.0.0
| `funnel_data.csv` | 6 | Marketing funnel stages and conversion rates |
| `customer_journey.csv` | 8 | Multi-touchpoint customer paths |
| `correlation_matrix.csv` | 10x10 | Pre-computed metric correlations |

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Project Structure
```
your_project/
├── data/
│   ├── campaign_performance.csv
│   ├── customer_data.csv
│   ├── ... (all CSV files)
├── app.py (or streamlit_starter_app.py)
├── requirements.txt
└── README.md
```

### 3. Run the Dashboard
```bash
streamlit run streamlit_starter_app.py
```

---

## 📈 Data Insights Built Into Dataset

### Campaign Performance
- **Seasonality**: Diwali (Oct-Nov) and Christmas (Dec) show 30-40% revenue boost
- **Weekend Effects**: Social media performs better on weekends; LinkedIn drops 40%
- **Channel Patterns**: Email has highest CVR; Google Ads highest volume

### Customer Data
- **Segment Profiles**: Premium customers have 2.5x higher LTV
- **Churn Indicators**: Low satisfaction + high support tickets = churn risk
- **Age-Income Correlation**: Peak income at age 45-50

### Product Sales
- **Category Performance**: Electronics highest volume; Fashion highest margins
- **Regional Variations**: West and South regions outperform
- **Quarterly Patterns**: Q4 electronics surge; Q2-Q3 fashion surge

### ML Model (Lead Scoring)
- **AUC**: ~0.75-0.80 (good predictive performance)
- **Key Features**: Webinar attendance and form submissions are strongest predictors
- **Learning Curve**: Model is well-calibrated, slight variance remains

---

## 📊 Visualization Mapping

| Chart Type | Data Source | Key Columns |
|------------|-------------|-------------|
| Bar Chart | campaign_performance | channel, revenue |
| Grouped Bar | campaign_performance | region, quarter, revenue |
| Stacked Bar | campaign_performance | month, campaign_type, spend |
| Line Chart | campaign_performance | date, revenue |
| Area Chart | campaign_performance | date, channel, conversions |
| Histogram | customer_data | age |
| Box Plot | customer_data | customer_segment, lifetime_value |
| Violin Plot | customer_data | nps_category, satisfaction_score |
| Scatter Plot | customer_data | income, lifetime_value, customer_segment |
| Bubble Chart | campaign_performance (agg) | ctr, conversion_rate, spend |
| Heatmap | correlation_matrix | all columns |
| Calendar Heatmap | campaign_performance | date, revenue |
| Pie/Donut | channel_attribution | channel, model columns |
| Treemap | product_sales | category, subcategory, product_name, sales |
| Sunburst | customer_data | region, city_tier, customer_segment |
| Funnel | funnel_data | stage, visitors |
| Choropleth | geographic_data | state, latitude, longitude, revenue |
| Bubble Map | geographic_data | latitude, longitude, store_count, satisfaction |
| Confusion Matrix | lead_scoring_results | actual_converted, predicted_class |
| ROC Curve | lead_scoring_results | actual_converted, predicted_probability |
| Learning Curve | learning_curve | training_size, train_score, validation_score |
| Feature Importance | feature_importance | feature, importance |

---

## 🎯 Assignment Deliverables

1. **Streamlit Dashboard** - All 20+ visualizations
2. **Source Code** - Well-documented Python files
3. **Insights Report** - 2-page business insights summary
4. **Presentation** - 5-minute video walkthrough

---

## 📧 Questions?

Contact your course instructor.

**Good luck! Let data tell the story.** 📊✨
