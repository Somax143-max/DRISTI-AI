# ==============================================================================
# DRISHTI AI: Production Multi-Stage Docker Container (SIH26038)
# Base: Ubuntu 22.04 LTS with Python 3.11 & CPU PyTorch
# ==============================================================================

FROM python:3.11-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /install

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU and core requirements
RUN pip install --no-cache-dir --prefix=/install/root \
    torch==2.1.2+cpu --extra-index-url https://download.pytorch.org/whl/cpu \
    opencv-python-headless==4.8.1.78 \
    numpy==1.26.2 \
    scipy==1.11.4 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2 \
    pydicom==2.4.4

# ==============================================================================
# Final Production Runtime Stage
# ==============================================================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy installed Python site-packages
COPY --from=builder /install/root /usr/local

# Runtime OS libraries for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy DRISHTI AI Application files
COPY . /app

# Non-root user for security
RUN useradd -m -u 1001 drishti && \
    chown -R drishti:drishti /app

USER drishti

EXPOSE 7860
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:7860/api/health || curl -f http://localhost:8080/api/health || exit 1

CMD ["python", "run_server.py", "7860"]

