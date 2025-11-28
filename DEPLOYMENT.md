# Deployment Guide - COVID-19 Vaccine Tracker

## Option 1: Streamlit Community Cloud (Recommended - FREE)

This is the easiest way to deploy your dashboard publicly.

### Prerequisites

- GitHub account
- Git installed on your computer

### Step-by-Step Instructions

#### 1. Create a GitHub Repository

```bash
# Navigate to your project folder
cd "C:\Users\Manish\Desktop\COVID-19 vaccine tracker"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - COVID-19 Vaccine Tracker"

# Create a new repository on GitHub (https://github.com/new)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/covid-vaccine-tracker.git
git branch -M main
git push -u origin main
```

#### 2. Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the details:
   - **Repository**: Select your `covid-vaccine-tracker` repo
   - **Branch**: `main`
   - **Main file path**: `app/streamlit_app.py`
5. Click "Deploy!"

⏱️ Deployment takes 2-5 minutes. You'll get a public URL like:
`https://your-username-covid-vaccine-tracker.streamlit.app`

### Important Notes

- **Data refresh**: The dashboard will download fresh data on first load
- **Free tier limits**: Suitable for moderate traffic (fine for demonstration purposes)
- **Updates**: Push changes to GitHub, and the app auto-redeploys

---

## Option 2: Docker Deployment

If you prefer containerized deployment:

```bash
# Build the Docker image
docker build -t covid-tracker .

# Run locally
docker run -p 8501:8501 covid-tracker

# For cloud deployment, push to:
# - Docker Hub
# - AWS ECS
# - Google Cloud Run
# - Azure Container Instances
```

---

## Option 3: Traditional Hosting

### Requirements

- Python 3.10+
- Public server (VPS, AWS EC2, etc.)

### Deployment Steps

```bash
# Install dependencies
pip install -r requirements.txt

# Run with nohup for background execution
nohup streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
```

---

## Troubleshooting

### Database Issues

If deployment shows "missing data" errors:

```bash
# Force data refresh
python fix_missing_data.py
```

### Memory Limits (Streamlit Cloud)

Free tier has 1GB RAM. If you hit limits:

- Reduce data caching duration in `streamlit_app.py`
- Consider upgrading to Streamlit Pro

---

## Security Considerations

- No sensitive data is stored
- All data is public (from Our World in Data)
- No authentication required
- HTTPS enabled by default on Streamlit Cloud

---

## Next Steps After Deployment

1. Share your public URL
2. Monitor app performance at Streamlit dashboard
3. Set up automated daily data updates (optional)
4. Add custom domain (Streamlit Pro feature)
