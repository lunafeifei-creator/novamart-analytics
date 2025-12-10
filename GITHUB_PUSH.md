# GitHub Push & Streamlit Cloud Setup Guide

## 🚀 Push Your Project to GitHub

Follow these steps to push your NovaMart Analytics Dashboard to GitHub and deploy to Streamlit Cloud.

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `novamart-analytics-dashboard`
3. Description: "Interactive Streamlit dashboard for NovaMart marketing analytics"
4. Choose Public (or Private if preferred)
5. **Do NOT** initialize with README (we have one)
6. Click "Create repository"

### Step 2: Configure Git Locally

```bash
# Navigate to your project directory
cd d:\Dubai\assignment\Dav2

# Initialize git (if not already done)
git init

# Configure user (if not already configured)
git config user.name "Your Name"
git config user.email "your.email@github.com"

# Or set globally
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"
```

### Step 3: Add Files to Git

```bash
# Add all files
git add .

# Check what will be committed
git status

# Expected: All files shown in green
```

### Step 4: Commit Changes

```bash
# Create initial commit
git commit -m "Initial commit: NovaMart Marketing Analytics Dashboard

- Comprehensive Streamlit dashboard for marketing analytics
- 7 interactive pages covering campaigns, customers, products, and ML models
- 20+ visualization types with interactive filters
- Ready for deployment to Streamlit Cloud"
```

### Step 5: Connect to Remote Repository

```bash
# Add remote origin (replace with your GitHub URL)
git remote add origin https://github.com/YOUR-USERNAME/novamart-analytics-dashboard.git

# Verify connection
git remote -v
```

### Step 6: Push to GitHub

```bash
# Rename main branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main

# First time may ask for authentication
# Use Personal Access Token if 2FA enabled:
# https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
```

### Step 7: Verify on GitHub

1. Visit https://github.com/YOUR-USERNAME/novamart-analytics-dashboard
2. Verify all files are there
3. Check that README.md displays properly

## 🌐 Deploy to Streamlit Cloud

### Step 1: Sign Up for Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Streamlit Cloud to access your GitHub

### Step 2: Deploy Your App

1. Go to https://share.streamlit.io/
2. Click "New app" button
3. Fill in the deployment form:

   **Repository**: YOUR-USERNAME/novamart-analytics-dashboard
   **Branch**: main
   **Main file path**: app.py

4. Click "Deploy!"

Streamlit will automatically:
- Clone your repository
- Install dependencies from requirements.txt
- Run your app
- Assign a public URL

### Step 3: Share Your Dashboard

Your app will be live at a URL like:
```
https://novamart-analytics-dashboard.streamlit.app
```

Or a shorter custom URL if you set one up.

## 📝 Best Practices for GitHub

### What to Commit ✅
- Python source files (.py)
- Configuration files (.toml, .yaml, .json)
- Documentation (README.md, .md files)
- Requirements file (requirements.txt)
- .gitignore file
- LICENSE file

### What NOT to Commit ❌
- CSV data files (too large, can add later)
- .streamlit/secrets.toml (sensitive data)
- __pycache__ folders (automatically ignored)
- .venv/ directories (automatically ignored)
- IDE config files (VS Code, PyCharm settings)

The `.gitignore` file should already handle these.

## 🔄 Making Updates

### After Making Changes Locally

```bash
# See what changed
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add new visualization: Customer cohort analysis"

# Push to GitHub
git push origin main
```

Streamlit Cloud will **automatically redeploy** when you push!

## 📊 Adding Data Files Later

If your CSV files are small (< 100MB total):

```bash
# Add CSV files
git add *.csv

# Commit
git commit -m "Add marketing analytics data files"

# Push
git push origin main
```

If files are too large:
- Use Git LFS (Large File Storage)
- Or skip CSV files and load from cloud storage
- Or upload to Streamlit secrets

## 🔒 Keeping Secrets Secure

Never commit sensitive data:

```bash
# Good: Secrets stored in Streamlit Cloud secrets panel
password = st.secrets["database_password"]

# Bad: Never do this
password = "actual_password_123"  # DON'T COMMIT THIS!
```

For Streamlit Cloud:
1. Deploy your app
2. Click settings (⚙️)
3. Go to "Secrets" tab
4. Paste your secrets.toml content (without file)

## 📈 Monitoring Your Deployment

### View App Metrics
1. Go to https://share.streamlit.io/
2. Click your app
3. View:
   - Total views
   - Active users
   - Memory usage
   - Performance metrics

### View Logs
1. Click settings (⚙️) in top-right of app
2. Click "Logs"
3. See recent errors/output

### Rerun App
1. Click "Rerun" button to force refresh
2. Useful if something seems stuck

## 🐛 Troubleshooting GitHub Push

### "fatal: not a git repository"
```bash
git init
```

### "remote: Permission denied"
- Check GitHub username/token
- For HTTPS: Use Personal Access Token
- For SSH: Set up SSH keys

### "rejected: main is behind"
```bash
# Pull latest changes first
git pull origin main

# Then push
git push origin main
```

### Files not appearing on GitHub
```bash
# Make sure you committed
git commit -m "Add files"

# Check status
git status

# Should be: "nothing to commit, working tree clean"
```

## 🎯 Streamlit Cloud Tips

### Custom Domain
Settings → General → Custom domain

### Environment Variables
Set in Streamlit Cloud settings panel:
```
PYTHONPATH=/mount/...
```

### Increase App Resources
Settings → App resources → Upgrade to Streamlit+ (paid)

### Share with Others
- Public app: Anyone with URL can view
- Private: Invite specific GitHub users
- Set in App settings → Sharing

## ✅ Verification Checklist

- [ ] All Python files committed to GitHub
- [ ] CSV files optional (on GitHub or in cloud storage)
- [ ] requirements.txt is accurate
- [ ] README.md displays correctly on GitHub
- [ ] .gitignore configured
- [ ] No secrets in code
- [ ] Streamlit Cloud authentication successful
- [ ] App deployed and accessible
- [ ] Share URL with team

## 🎉 Success!

Your dashboard is now:
- ✅ Version controlled on GitHub
- ✅ Publicly accessible on Streamlit Cloud
- ✅ Auto-updating with each push
- ✅ Sharable with stakeholders

## 📞 Need Help?

- **GitHub Docs**: https://docs.github.com
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-cloud
- **Streamlit Community**: https://discuss.streamlit.io

---

**Congratulations!** Your analytics dashboard is live! 🚀
