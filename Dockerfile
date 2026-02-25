# ---- deps stage: create venv with uv ----
    FROM python:3.12-slim-bookworm AS deps

    WORKDIR /app
    
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        PIP_NO_CACHE_DIR=1 \
        UV_CACHE_DIR=/tmp/uv-cache
    
    # (مهم) بعض البكجات تحتاج build tools
    RUN apt-get update && apt-get install -y --no-install-recommends \
          build-essential gcc \
        && rm -rf /var/lib/apt/lists/*
    
    COPY pyproject.toml uv.lock ./
    
    RUN pip install --no-cache-dir uv \
        && uv venv /opt/venv \
        && . /opt/venv/bin/activate \
        && uv sync --frozen --no-dev \
        && rm -rf /tmp/uv-cache
    
    # ---- runtime stage: chromium + run tests ----
    FROM python:3.12-slim-bookworm
    
    WORKDIR /app
    
    # Chromium and runtime libs
    RUN apt-get update \
        && apt-get install -y --no-install-recommends \
            chromium \
            chromium-driver \
            libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
            libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
            libgbm1 libasound2 libpango-1.0-0 libcairo2 \
        && rm -rf /var/lib/apt/lists/*
    
    ENV CHROMIUM_BIN=/usr/bin/chromium \
        RUNNING_IN_DOCKER=1 \
        PATH="/opt/venv/bin:$PATH"
    
    # Copy venv from deps stage
    COPY --from=deps /opt/venv /opt/venv
    
    # Copy project
    COPY . .
    
    RUN pip install --no-cache-dir uv
    CMD ["uv", "run", "pytest", "-v"]