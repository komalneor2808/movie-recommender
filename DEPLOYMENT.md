# Deployment Guide

## Quick Deploy to Streamlit Community Cloud (Recommended)

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: komalneor2808/movie-recommender
5. Branch: main
6. Main file: app.py
7. Click "Deploy!"

Your app will be live at: https://[your-app-name].streamlit.app

## Alternative: Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select movie-recommender repository
5. Railway auto-deploys Python apps

## Alternative: Render

1. Go to https://render.com
2. Sign up with GitHub
3. New + → Web Service
4. Connect GitHub repo
5. Build Command: pip install -r requirements.txt
6. Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0

## Notes

- All platforms support SQLite databases
- Deployment takes 2-5 minutes
- Free tiers available on all platforms
- Automatic updates when you push to GitHub
