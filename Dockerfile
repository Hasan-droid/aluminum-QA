# alumnium_tests – Python 3.12 + Chromium for Alumnium/Selenium
FROM python:3.12-bookworm

# Chromium and runtime libs (from README + headless)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
        libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
        libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Use apt Chromium path (conftest reads CHROMIUM_BIN)
ENV CHROMIUM_BIN=/usr/bin/chromium
# Run browser headless in container
ENV RUNNING_IN_DOCKER=1

WORKDIR /app

# Install uv and sync project (uses pyproject.toml + uv.lock)
COPY pyproject.toml uv.lock ./
RUN pip install uv \
    && uv sync --frozen --no-dev

COPY . .

# Default: run all tests. Override with docker run ... pytest <args>
CMD ["uv", "run", "pytest", "-v" ]
