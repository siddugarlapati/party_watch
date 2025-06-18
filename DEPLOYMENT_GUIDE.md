# 🚀 PartyWatch Deployment Guide

## **Option 1: Streamlit Cloud (Frontend Only) - EASIEST**

### ✅ What Works:
- YouTube player with video embedding
- Room creation and joining
- Chat functionality
- Sprint board and meeting notes
- Work mode features

### ❌ Limitations:
- No real-time sync between users
- Each user sees their own data
- No persistent storage

### 🚀 Deploy Steps:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set main file path: `streamlit_app.py`
4. Deploy!

## **Option 2: Render (Full Stack) - RECOMMENDED**

### ✅ What Works:
- Everything from Option 1 PLUS:
- Real-time collaboration
- Shared rooms between users
- Persistent data storage
- Video sync between users

### 🚀 Deploy Steps:

#### Step 1: Deploy Backend
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r backend/requirements.txt`
5. Set start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy and note the URL (e.g., `https://your-backend.onrender.com`)

#### Step 2: Deploy Frontend
1. In Render, create another Web Service
2. Connect same GitHub repository
3. Set build command: `pip install -r requirements_streamlit.txt`
4. Set start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variable:
   - Key: `BACKEND_URL`
   - Value: `https://your-backend.onrender.com/api`
6. Deploy!

## **Option 3: Railway (Alternative)**

### 🚀 Deploy Steps:
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Railway will auto-detect and deploy both services
4. Set environment variables as needed

## **🎯 Quick Test:**

### For Frontend Only:
```bash
# Run locally
streamlit run streamlit_app.py
```

### For Full Stack:
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
streamlit run streamlit_app.py
```

## **🔧 What You Get:**

### YouTube Features:
- ✅ Video embedding and playback
- ✅ Room creation with video URLs
- ✅ Host can change videos
- ✅ Chat during watching
- ✅ Video URL display

### Work Mode Features:
- ✅ Sprint board (Kanban)
- ✅ Meeting notes
- ✅ Video calls (Jitsi Meet)
- ✅ Professional UI

### Real-time Features (with backend):
- ✅ Shared chat
- ✅ Shared sprint board
- ✅ Shared meeting notes
- ✅ Room synchronization

## **🎉 You're Ready!**

**For immediate use**: Deploy to Streamlit Cloud
**For full collaboration**: Deploy to Render with backend

Both options will give you a working YouTube watch party app! 🎬 