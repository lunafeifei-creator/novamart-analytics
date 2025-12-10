# Deployment Guide - Streamlit Cloud

## 🌐 Deploy NovaMart Analytics Dashboard to Streamlit Cloud

This guide walks you through deploying your dashboard to Streamlit Cloud for free hosting.

## Prerequisites

✅ GitHub account  
✅ Code pushed to GitHub repository  
✅ Streamlit Cloud account (sign up at streamlit.io/cloud)

## Step-by-Step Deployment

### 1. Prepare Your GitHub Repository

```bash
# Initialize Git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "NovaMart Analytics Dashboard - Initial Release"

# Add remote repository
git remote add origin https://github.com/yourusername/novamart-analytics.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Sign Up for Streamlit Cloud

- Visit: https://streamlit.io/cloud
- Click "Sign Up"
- Authorize with GitHub
- Accept permissions

### 3. Deploy Your App

1. Go to https://share.streamlit.io/
2. Click "New app" button
3. Fill in the form:
   - **Repository**: yourusername/novamart-analytics
   - **Branch**: main
   - **Main file path**: app.py
4. Click "Deploy"

The dashboard will build and deploy (2-5 minutes).

### 4. Share Your Dashboard

Once deployed, Streamlit gives you a URL like:
```
https://novamart-analytics.streamlit.app
```

Share this link with stakeholders!

## 📊 Managing Your Deployed App

### View Logs
- Click settings icon (⚙️) in top-right
- Check "Logs" tab for any errors

### Rerun App
- Click "Rerun" button (↻) to manually refresh

### Update Code
Simply push new changes to GitHub:
```bash
git add .
git commit -m "Update visualizations"
git push origin main
```

Streamlit automatically redeploys!

### Configure Secrets
If you use API keys or sensitive data:

1. Click settings (⚙️) → "Secrets"
2. Add `secrets.toml` file locally:
```toml
# .streamlit/secrets.toml
database_password = "your-password"
api_key = "your-api-key"
```

3. Access in code:
```python
password = st.secrets["database_password"]
```

## 🔧 Advanced Configuration

### Set Custom Domain
- Streamlit Cloud > App settings > Custom domain
- Add your domain (requires DNS setup)

### Environment Variables
In `.streamlit/config.toml`:
```toml
[client]
showErrorDetails = true

[logger]
level = "info"
```

### Memory & Performance
- Default: 1GB RAM
- For larger datasets, upgrade to Pro plan
- Monitor usage in app analytics

## 📈 Monitoring & Analytics

1. Go to app dashboard
2. View metrics:
   - Total views
   - Active users
   - Performance
   - Traffic

## ⚠️ Troubleshooting Deployment

### "Build failed" error
- Check if all dependencies are in `requirements.txt`
- Ensure Python files have no syntax errors
- Check that CSV files are accessible

### "Module not found" on cloud
- Verify package names in requirements.txt
- Use `pip list` to get exact versions:
```bash
pip freeze > requirements.txt
```

### Dashboard runs slowly on cloud
- Optimize data loading (use data caching)
- Reduce CSV file sizes
- Use `@st.cache_data` for expensive operations

### CSV files not found
Option 1: Add to GitHub
```bash
git add *.csv
git commit -m "Add data files"
git push
```

Option 2: Download from cloud
Modify `app.py`:
```python
import streamlit as st

@st.cache_data
def load_data():
    # Download from cloud storage
    df = pd.read_csv('https://your-storage/file.csv')
    return df
```

## 🔄 CI/CD Integration

For automatic deployments on code push:

1. GitHub Actions workflow (`.github/workflows/deploy.yml`):
```yaml
name: Deploy to Streamlit Cloud
on:
  push:
    branches: [ main ]
jobs:
  streamlit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Streamlit deploy
        uses: blackary/streamlit-demo-action@master
        with:
          app-path: app.py
```

## 📋 Pre-Deployment Checklist

- [ ] All code commits pushed to main branch
- [ ] `requirements.txt` updated with all dependencies
- [ ] `app.py` tested locally with `streamlit run app.py`
- [ ] CSV files paths are correct
- [ ] No hardcoded secrets or passwords
- [ ] README.md updated with deployment info
- [ ] `.gitignore` configured properly

## 🚀 Performance Tips for Cloud

1. **Cache everything**:
```python
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')
```

2. **Use efficient data operations**:
```python
# Good
df[df['column'] > 100]

# Avoid
for row in df:
    if row['column'] > 100:
        ...
```

3. **Limit data shown**:
```python
# Show only necessary rows
df.head(1000)
```

## 📞 Support

- Streamlit Cloud docs: https://docs.streamlit.io/streamlit-cloud
- Community forum: https://discuss.streamlit.io
- GitHub issues: Post in your repo

## ✨ Next Steps

1. Monitor app performance
2. Gather user feedback
3. Add more features/visualizations
4. Upgrade plan if needed

---

**Congratulations!** Your NovaMart Analytics Dashboard is now live! 🎉
