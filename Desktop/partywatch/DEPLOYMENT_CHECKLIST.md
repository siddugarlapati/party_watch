# ✅ PartyWatch Deployment Checklist

## **Pre-Deployment**
- [ ] Code pushed to GitHub
- [ ] Repository structure verified
- [ ] All files present and correct

## **Backend Deployment (Render)**
- [ ] Render account created
- [ ] New Web Service created
- [ ] GitHub repository connected
- [ ] Build command set: `pip install -r backend/requirements.txt`
- [ ] Start command set: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variable added: `PYTHON_VERSION=3.11.0`
- [ ] Backend deployed successfully
- [ ] Backend URL noted: `https://your-backend-name.onrender.com`
- [ ] Backend tested (shows API message)

## **Frontend Deployment (Render)**
- [ ] New Web Service created for frontend
- [ ] Same GitHub repository connected
- [ ] Build command set: `pip install -r requirements_streamlit.txt`
- [ ] Start command set: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- [ ] Environment variable added: `BACKEND_URL=https://your-backend-name.onrender.com/api`
- [ ] Environment variable added: `PYTHON_VERSION=3.11.0`
- [ ] Frontend deployed successfully
- [ ] Frontend URL noted: `https://your-frontend-name.onrender.com`

## **Testing**
- [ ] Frontend loads correctly
- [ ] Can create YouTube room
- [ ] YouTube video plays
- [ ] Chat works
- [ ] Room joining works
- [ ] Work mode features work
- [ ] Real-time collaboration tested (2 browsers)

## **Final Verification**
- [ ] Both services running
- [ ] No error messages in logs
- [ ] All features functional
- [ ] Ready to share with users

## **🎉 Deployment Complete!**
- [ ] Share frontend URL with friends
- [ ] Test with multiple users
- [ ] Enjoy your PartyWatch app! 🎬 