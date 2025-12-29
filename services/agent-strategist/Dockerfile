# --- STAGE 1: Builder ---
FROM python:3.14-slim AS builder
WORKDIR /build

# Grab the strategist-specific requirements
COPY services/agent-strategist/requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt

# --- STAGE 2: Runtime ---
FROM python:3.14-slim
WORKDIR /app

COPY --from=builder /install /usr/local
COPY services/agent-strategist/app ./app
COPY shared /shared
RUN pip install -e /shared

ENV RENDER=false PYTHONOPTIMIZE=1
RUN adduser --disabled-password --gecos "" superjack_user
USER superjack_user

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]