# 🚀 Deploy Your AI Frontend to Vercel

## Step-by-Step Deployment Guide

### Method 1: Quick Deploy (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to Frontend**
   ```bash
   cd frontend
   ```

3. **Install Dependencies**
   ```bash
   npm install
   ```

4. **Set Environment Variable**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local and set your backend URL
   ```

5. **Deploy to Vercel**
   ```bash
   vercel
   ```
   - Follow the prompts
   - Choose "Yes" to deploy
   - Set project name
   - Deploy!

### Method 2: GitHub Integration

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add frontend"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Sign in with GitHub
   - Click "New Project"
   - Import your repository
   - Set root directory to `frontend`
   - Add environment variable: `NEXT_PUBLIC_API_URL`
   - Deploy!

### Environment Variables

For production, set these in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend Deployment Options

Your backend can be deployed to:
- **Render.com** (Free tier available)
- **Railway** (Easy deployment)
- **Fly.io** (Good performance)
- **Heroku** (Popular choice)

### Complete Setup Example

1. **Deploy Backend to Render.com**
   - Connect GitHub repo
   - Set environment variables
   - Get your backend URL

2. **Deploy Frontend to Vercel**
   - Set `NEXT_PUBLIC_API_URL` to your backend URL
   - Deploy frontend

3. **Test Everything**
   - Visit your Vercel URL
   - Try all AI features
   - Enjoy your live AI app!

## 🎉 Result

You'll have a beautiful web interface that anyone can use without PowerShell!

**Example URLs:**
- Frontend: https://your-app.vercel.app
- Backend: https://your-backend.render.com

Users can simply visit your website and use all AI features through a friendly interface!