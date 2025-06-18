# 🚀 PartyWatch Deployment Guide

Deploy PartyWatch for free and share it with your friends!

## Option 1: Streamlit Cloud (Recommended - Easiest)

### Step 1: Prepare Your Code
1. Create a GitHub repository
2. Upload these files to your repo:
   - `streamlit_app.py` (main app file)
   - `requirements_streamlit.txt` (dependencies)
   - `README.md` (optional)

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app.py`
6. Click "Deploy"

### Step 3: Share with Friends
- Your app will be available at: `https://your-app-name.streamlit.app`
- Share this URL with your friends!

## Option 2: Render (Free Backend + Frontend)

### Step 1: Prepare Backend
1. Create a GitHub repository
2. Add these files:
   - `backend/app/main.py`
   - `backend/requirements.txt`
   - `render.yaml` (for Render configuration)

### Step 2: Deploy Backend
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your repository
5. Set build command: `pip install -r backend/requirements.txt`
6. Set start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
7. Deploy

### Step 3: Deploy Frontend
1. In Render, create another Web Service
2. Use the same repository
3. Set build command: `pip install -r requirements_streamlit.txt`
4. Set start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variable: `BACKEND_URL=https://your-backend-url.onrender.com/api`

## Option 3: Railway (Alternative)

### Step 1: Prepare for Railway
1. Create `railway.json` configuration file
2. Push to GitHub

### Step 2: Deploy
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy automatically

## Option 4: Heroku (Free Tier Discontinued)

Note: Heroku no longer offers a free tier, but you can use it if you have a paid account.

## Quick Start Commands

```bash
# Clone your repository
git clone https://github.com/yourusername/partywatch.git
cd partywatch

# For Streamlit Cloud (simplest)
# Just upload streamlit_app.py and requirements_streamlit.txt

# For full deployment with backend
# Upload all files and configure environment variables
```

## Environment Variables

For full deployment, set these environment variables:

```bash
BACKEND_URL=https://your-backend-url.com/api
```

## Features Available in Deployed Version

### Party Mode:
- ✅ Create/Join rooms
- ✅ Real-time chat
- ✅ Room codes
- ✅ User presence

### Work Mode:
- ✅ Sprint board (Kanban)
- ✅ Meeting notes
- ✅ Video calls (Jitsi Meet)
- ✅ Professional UI
- ✅ Settings panel

## Troubleshooting

### Common Issues:
1. **App not loading**: Check requirements.txt has all dependencies
2. **Backend connection error**: Verify BACKEND_URL environment variable
3. **Port issues**: Make sure to use `$PORT` environment variable

### Support:
- Check Streamlit Cloud logs for errors
- Verify all files are in the correct location
- Test locally first with `streamlit run streamlit_app.py`

## Sharing Your App

Once deployed, share these with your friends:
- **App URL**: Your deployed app link
- **Room Codes**: Generated when creating rooms
- **Video Call Links**: Generated in work mode

Happy watching! 🎬 