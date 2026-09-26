# ==============================================================================
# DRISHTI AI: Production Multi-Stage Docker Container (SIH26038)
# Base: Python 3.11 Slim with CPU PyTorch & OpenCV
# ==============================================================================

FROM python:3.11-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /install

# Install PyTorch CPU and core requirements into isolated prefix
RUN pip install --no-cache-dir --prefix=/install/root \
    torch==2.1.2+cpu --extra-index-url https://download.pytorch.org/whl/cpu \
    opencv-python-headless==4.8.1.78 \
    numpy==1.26.2 \
    scipy==1.11.4 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2 \
    pydicom==2.4.4 \
    Pillow==10.1.0

# ==============================================================================
# Final Production Runtime Stage
# ==============================================================================
FROM python:3.11-slim AS runner

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy installed Python site-packages
COPY --from=builder /install/root /usr/local

# Runtime OS libraries for OpenCV & Healthchecks (libgl1 replaces deprecated libgl1-mesa-glx)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy DRISHTI AI Application files
COPY . /app

# Non-root user for security
RUN useradd -m -u 1001 drishti && \
    chown -R drishti:drishti /app

USER drishti

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

CMD ["python", "run_server.py", "8080"]
