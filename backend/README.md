# ⚙️ DRISHTI-AI Backend

This folder contains the complete, self-contained AI inference server and clinical analysis pipeline for DRISHTI-AI.

## 📁 Directory Contents
- `server.py` & `run_server.py`: HTTP & REST API server
- `retina_analyzer.py`: PyTorch deep neural network and OpenCV clinical processing pipeline
- `retina_dr_grader.pth`: Diabetic Retinopathy 5-stage grader model weights
- `retina_eye_classifier.pth`: Retinal fundus eye verifier model weights
- `app/`: Production modules (input validation, drift monitoring, clinical report generation, security)
- `Dockerfile`: Production multi-stage Docker build
- `requirements.txt`: Python dependencies

## 🚀 Easy 1-Click Deployment Options

### Option 1: Deploy to Render.com (Free)
1. Go to [render.com](https://render.com) and click **New** -> **Web Service**.
2. Connect your GitHub repository `Somax143-max/DRISTI-AI`.
3. Set **Root Directory** to `backend`.
4. Set **Environment** to `Python 3` (or `Docker`).
5. Build command: `pip install -r requirements.txt`
6. Start command: `python run_server.py`
7. Click **Create Web Service**.

### Option 2: Deploy to Hugging Face Spaces (Free 16GB RAM)
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Choose **Docker** as Space SDK.
3. Push the contents of `backend/` to your Space repo.

### Option 3: Local Running
```bash
python run_server.py 8081
```
The server will start on `http://127.0.0.1:8081` and automatically serve the `../frontend` UI.
