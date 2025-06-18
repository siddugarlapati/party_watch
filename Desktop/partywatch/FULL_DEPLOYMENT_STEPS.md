# 🚀 Complete PartyWatch Deployment - Step by Step

## **Prerequisites**
- GitHub account
- Render account (free tier available)
- Your code pushed to GitHub

---

## **Step 1: Prepare Your GitHub Repository**

### 1.1 Push Your Code to GitHub
```bash
# If you haven't already
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 1.2 Verify Repository Structure
Your repository should have:
```
partywatch/
├── streamlit_app.py          # Frontend
├── requirements_streamlit.txt # Frontend dependencies
├── backend/
│   ├── app/
│   │   └── main.py          # Backend API
│   └── requirements.txt     # Backend dependencies
├── render.yaml              # Render configuration
└── DEPLOYMENT_GUIDE.md      # This guide
```

---

## **Step 2: Deploy Backend to Render**

### 2.1 Create Backend Service
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

**Basic Settings:**
- **Name**: `partywatch-backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
- `PYTHON_VERSION`: `3.11.0`

### 2.2 Deploy Backend
1. Click **"Create Web Service"**
2. Wait for deployment (2-3 minutes)
3. Note your backend URL: `https://your-backend-name.onrender.com`

---

## **Step 3: Deploy Frontend to Render**

### 3.1 Create Frontend Service
1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect the same GitHub repository
3. Configure the service:

**Basic Settings:**
- **Name**: `partywatch-frontend`
- **Environment**: `Python 3`
- **Region**: Same as backend
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements_streamlit.txt`
- **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

**Environment Variables:**
- `BACKEND_URL`: `https://your-backend-name.onrender.com/api`
- `PYTHON_VERSION`: `3.11.0`

### 3.2 Deploy Frontend
1. Click **"Create Web Service"**
2. Wait for deployment (2-3 minutes)
3. Your app will be available at: `https://your-frontend-name.onrender.com`

---

## **Step 4: Test Your Deployment**

### 4.1 Test Backend
1. Visit your backend URL
2. You should see: `{"message": "PartyWatch API is running!"}`

### 4.2 Test Frontend
1. Visit your frontend URL
2. Create a YouTube room
3. Test the video player
4. Test chat functionality

### 4.3 Test Full Functionality
1. Open your app in two different browsers/incognito windows
2. Create a room in one window
3. Join the room in the other window using the room code
4. Test real-time chat and collaboration

---

## **Step 5: Troubleshooting**

### Common Issues:

**Backend won't start:**
- Check build logs in Render
- Verify `backend/requirements.txt` exists
- Ensure `backend/app/main.py` exists

**Frontend can't connect to backend:**
- Verify `BACKEND_URL` environment variable
- Check backend is running
- Test backend URL directly

**YouTube player not working:**
- Check browser console for errors
- Verify video URL format
- Test with different YouTube URLs

---

## **Step 6: Custom Domain (Optional)**

### 6.1 Add Custom Domain
1. In Render dashboard, go to your service
2. Click **"Settings"** → **"Custom Domains"**
3. Add your domain
4. Update DNS records as instructed

---

## **🎉 Success!**

Your PartyWatch app is now fully deployed with:
- ✅ Real-time YouTube watch parties
- ✅ Shared chat and collaboration
- ✅ Sprint board and meeting notes
- ✅ Work mode features
- ✅ Persistent data storage

### **Your URLs:**
- **Frontend**: `https://your-frontend-name.onrender.com`
- **Backend**: `https://your-backend-name.onrender.com`

### **Share with Friends:**
- Send them the frontend URL
- They can join your rooms using room codes
- Real-time collaboration works across all users!

---

## **Need Help?**

If you encounter issues:
1. Check Render deployment logs
2. Verify all files are in the correct locations
3. Test locally first: `streamlit run streamlit_app.py`
4. Check the troubleshooting section above

**Your PartyWatch app is ready to use! 🎬** 