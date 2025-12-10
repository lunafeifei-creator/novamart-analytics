# Quick Start Guide - NovaMart Analytics Dashboard

## 📋 Prerequisites

- Python 3.8+
- Git
- pip (comes with Python)

## ⚡ Quick Setup (5 minutes)

### Step 1: Clone/Download Project
```bash
# If using Git:
git clone <your-repo-url>
cd novamart-analytics

# Or just download and extract the folder
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Prepare Data
Place all CSV files in the project root directory:
- campaign_performance.csv
- customer_data.csv
- product_sales.csv
- lead_scoring_results.csv
- feature_importance.csv
- learning_curve.csv
- geographic_data.csv
- channel_attribution.csv
- funnel_data.csv
- customer_journey.csv
- correlation_matrix.csv

### Step 5: Run Dashboard
```bash
streamlit run app.py
```

The dashboard will open at: **http://localhost:8501**

## 🧭 Navigation

1. **Executive Overview**: High-level KPIs and trends
2. **Campaign Analytics**: Campaign performance and temporal analysis
3. **Customer Insights**: Customer behavior and segmentation
4. **Product Performance**: Product hierarchy and sales analysis
5. **Geographic Analysis**: Regional performance and growth opportunities
6. **Attribution & Funnel**: Funnel visualization and attribution models
7. **ML Model Evaluation**: ML model performance and feature importance

## 🛠️ Troubleshooting

### Issue: "Module not found"
```bash
# Reinstall all requirements
pip install -r requirements.txt --upgrade
```

### Issue: "CSV files not found"
- Check file names match exactly
- Ensure files are in project root directory
- On Windows, use forward slashes in paths

### Issue: Dashboard runs slowly
- This is normal for first load (data caching)
- Subsequent loads are much faster
- Clear cache if needed: `streamlit cache clear`

## 📚 File Structure

```
project/
├── app.py                    ← Run this file (contains all 7 pages)
├── config.py                 ← Edit for colors/settings
├── requirements.txt          ← Dependencies
├── data/                     ← CSV data files
├── visualizations/           ← Chart functions
├── .streamlit/
│   └── config.toml          ← Streamlit settings
└── README.md                 ← Full documentation
```

## 🚀 Next Steps

1. Explore each page to understand the visualizations
2. Modify colors in `config.py` if needed
3. Add custom filters or metrics in page files
4. Deploy to Streamlit Cloud (see DEPLOYMENT.md)

## 💡 Tips

- Use filters to focus on specific channels, regions, or time periods
- Hover over charts for more detailed information
- Click on category labels in treemaps to drill down
- Export charts using the camera icon in top-right of each chart

## 📞 Need Help?

- Check README.md for detailed documentation
- Review example code in `visualizations/charts.py`
- Read Streamlit docs: https://docs.streamlit.io
