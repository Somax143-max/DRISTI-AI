# 🌐 DRISHTI-AI Frontend

This folder contains the complete, self-contained client-side web application for DRISHTI-AI.

## 🚀 Easy 1-Click Deployment Options

### Option 1: Deploy to Vercel (Recommended)
1. Go to [vercel.com](https://vercel.com) and click **Add New Project**.
2. Select your repository `Somax143-max/DRISTI-AI`.
3. Set **Root Directory** to `frontend`.
4. Click **Deploy**. Vercel will build and give you a public URL (e.g. `https://drishti-ai.vercel.app`).

### Option 2: Deploy to Netlify
1. Go to [netlify.com](https://netlify.com) and click **Add new site** -> **Import an existing project**.
2. Select your GitHub repository.
3. Set **Base directory** to `frontend`.
4. Click **Deploy site**.

### Option 3: Connect to Backend API
By default, the frontend automatically routes API calls to:
1. `https://drishti-ai-backend.onrender.com` (via `vercel.json` rewrite or default backend URL), OR
2. Any backend URL by adding `?api=https://your-backend-url` to the URL.
