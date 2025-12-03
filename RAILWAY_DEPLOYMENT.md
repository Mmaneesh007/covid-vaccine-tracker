# 🚂 Deploying FastAPI to Railway.app

This guide walks you through deploying your FastAPI backend to Railway.app for free public hosting.

---

## 🎯 What You'll Get

After deployment, your API will be publicly accessible at:

```
https://your-project-name.up.railway.app/api/v1
```

**Benefits:**

- ✅ Free hosting (500 hours/month on free tier)
- ✅ Auto-deploy from GitHub
- ✅ HTTPS by default
- ✅ Environment variables support
- ✅ Logs and monitoring dashboard

---

## 📋 Prerequisites

1. **GitHub Account** (you already have this!)
2. **Railway Account** (we'll create this)

---

## 🚀 Deployment Steps

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app/)
2. Click **"Start a New Project"** or **"Login with GitHub"**
3. Authorize Railway to access your GitHub repos

### Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `Mmaneesh007/covid-vaccine-tracker`
4. Railway will detect your `railway.json` configuration automatically

### Step 3: Configure Environment (Optional)

Railway will use these defaults:

- **Build Command**: Automatically installs dependencies
- **Start Command**: `uvicorn app.experimental.main:app --host 0.0.0.0 --port $PORT`

No environment variables are required! The app uses SQLite which is included in your repo.

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for the build to complete
3. Railway will provide you a public URL

---

## 🔗 Getting Your API URL

After deployment:

1. Go to your Railway dashboard
2. Click on your deployed service
3. Go to **"Settings"** → **"Domains"**
4. You'll see something like: `https://covid-vaccine-tracker-api-production.up.railway.app`

This is your public API base URL!

---

## ✅ Testing Your Deployed API

### Test in Browser

Visit these URLs (replace with your actual Railway URL):

```
https://your-project.up.railway.app/health
https://your-project.up.railway.app/api/v1/countries
https://your-project.up.railway.app/docs
```

### Test with Python

```python
import requests

# Replace with your Railway URL
BASE_URL = "https://your-project.up.railway.app/api/v1"

# Get countries
response = requests.get(f"{BASE_URL}/countries")
print(response.json())

# Get India stats
response = requests.get(f"{BASE_URL}/countries/India")
print(response.json())
```

---

## 📝 Update Your Documentation

After deployment, update the following:

### 1. Update `examples/basic_queries.py`

Change:

```python
BASE_URL = "http://localhost:8000/api/v1"
```

To:

```python
BASE_URL = "https://your-actual-railway-url.up.railway.app/api/v1"
```

### 2. Update Streamlit "Developers" Page

In `app/streamlit_app.py`, update the API URL in the documentation.

### 3. Update README.md

Add the public API URL to your main README.

---

## 🔄 Auto-Deploy on Push

Railway automatically deploys whenever you push to GitHub!

```bash
git add .
git commit -m "Update API endpoints"
git push origin main
```

Railway will detect the push and redeploy within 2-3 minutes.

---

## 📊 Monitoring

### View Logs

1. Go to Railway dashboard
2. Click on your service
3. Click **"Deployments"** → Select latest deployment
4. View real-time logs

### Metrics

Railway shows:

- CPU usage
- Memory usage
- Request count
- Error rate

---

## 💰 Free Tier Limits

Railway's free tier includes:

- **500 hours/month** execution time
- **100 GB** bandwidth
- **1 GB** RAM per service

This is more than enough for a portfolio project!

---

## 🐛 Troubleshooting

### Build Fails

**Error**: `Module not found`
**Fix**: Ensure all dependencies are in `requirements.txt` and `requirements-api.txt`

### Service Crashes

**Error**: `Application startup failed`
**Fix**: Check logs in Railway dashboard. Usually a missing dependency or database issue.

### CORS Errors

**Error**: `Access-Control-Allow-Origin missing`
**Fix**: Already configured in `config.py` with your Streamlit Cloud domain.

---

## 🎉 You're Done

Your API is now:

- ✅ Publicly hosted
- ✅ Auto-deploying from GitHub
- ✅ Monitored and logged
- ✅ Free to use

Share your API URL with developers! 🚀
