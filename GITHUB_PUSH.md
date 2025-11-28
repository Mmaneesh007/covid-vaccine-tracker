# GitHub Push Instructions

Your code is ready to push! Follow these steps:

## Step 1: Create GitHub Repository

1. Open your browser and go to: **<https://github.com/new>**
2. Fill in the details:
   - **Repository name**: `covid-vaccine-tracker` (or your preferred name)
   - **Description**: "Real-time COVID-19 vaccination tracker with interactive visualizations and forecasting"
   - **Visibility**: Public ✅
   - **Do NOT** initialize with README, .gitignore, or license (we already have these)
3. Click **"Create repository"**

## Step 2: Push Your Code

GitHub will show you commands. **Use these instead** (they're already configured):

```bash
git branch -M main
git remote add origin https://github.com/Mmaneesh007/covid-vaccine-tracker.git
git push -u origin main
```

> **Note**: Replace `Mmaneesh007/covid-vaccine-tracker` with your actual GitHub username and repository name if different.

### If you get authentication errors

#### Option A: Use GitHub CLI (Easiest)

```bash
gh auth login
# Follow the prompts to authenticate
git push -u origin main
```

#### Option B: Use Personal Access Token

1. Go to <https://github.com/settings/tokens>
2. Click "Generate new token (classic)"
3. Give it a name like "COVID Tracker Deploy"
4. Select scope: `repo` (full control)
5. Generate and copy the token
6. When pushing, use:
   - Username: `Mmaneesh007`
   - Password: `<paste your token>`

## Step 3: Deploy to Streamlit Cloud

Once pushed to GitHub:

1. Go to **<https://share.streamlit.io/>**
2. Click **"New app"**
3. Select:
   - Repository: `Mmaneesh007/covid-vaccine-tracker`
   - Branch: `main`
   - Main file path: `app/streamlit_app.py`
4. Click **"Deploy!"**

Your app will be live at:
`https://mmaneesh007-covid-vaccine-tracker.streamlit.app`

---

## Quick Commands Reference

```bash
# Check status
git status

# View remote
git remote -v

# Push to GitHub
git push -u origin main

# If you need to update later
git add .
git commit -m "Updated dashboard"
git push
```

---

## ✅ What's Already Done

- ✅ Git repository initialized
- ✅ All files committed (32 files)
- ✅ `.gitignore` configured
- ✅ Streamlit config ready

**You're one command away from GitHub!** 🚀
