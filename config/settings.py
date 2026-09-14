"""
DRISHTI AI: Central Configuration & Environment Settings (Item 65, 66)
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Environment mode
ENV = os.environ.get("DRISHTI_ENV", "development")
DEBUG = (ENV == "development")

# Server settings
PORT = int(os.environ.get("DRISHTI_PORT", 8080))
HOST = os.environ.get("DRISHTI_HOST", "0.0.0.0")

# Security keys
SECRET_KEY = os.environ.get("DRISHTI_SECRET_KEY", "drishti-ai-production-secret-sih26038-change-in-prod")
SESSION_COOKIE_NAME = "drishti_session"
CSRF_COOKIE_NAME = "drishti_csrf"

# Rural edge mode settings
RURAL_EDGE_MODE = os.environ.get("RURAL_EDGE_MODE", "true").lower() == "true"
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024 # 50MB
CALIBRATION_TEMPERATURE = 1.12
ENTROPY_UNCERTAINTY_THRESHOLD = 0.60
FOCUS_UNGRADABLE_THRESHOLD = 12.0

# Paths
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DB_PATH = os.path.join(DATA_DIR, "drishti_clinical.db")
