# --- STAGE 1: The Builder ---
FROM python:3.14-slim AS builder
WORKDIR /build

# Explicitly grab requirements from the root context
COPY services/orchestrator/requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt

# --- STAGE 2: The Runtime ---
FROM python:3.14-slim
WORKDIR /app

# 1. THE SECRET SAUCE: Tell Python to look in /app for packages
ENV PYTHONPATH=/app \
    RENDER=false \
    PYTHONOPTIMIZE=1

# 2. Pull the optimized dependencies from Stage 1
COPY --from=builder /install /usr/local

# 3. Copy the code using the root-relative path
COPY services/orchestrator/app ./app
COPY agents /agents 
COPY shared /shared
RUN pip install -e /shared

RUN adduser --disabled-password --gecos "" superjack_user
USER superjack_user

EXPOSE 8001

# 4. Run as a module, not a script (2025 Standard)
CMD ["python", "-m", "app.main"]