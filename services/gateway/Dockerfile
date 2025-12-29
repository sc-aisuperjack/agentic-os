FROM python:3.14-slim AS builder
WORKDIR /build

COPY services/gateway/requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.14-slim
WORKDIR /app

COPY --from=builder /install /usr/local
COPY services/gateway/app ./app
COPY shared /shared
RUN pip install -e /shared

ENV RENDER=false PYTHONOPTIMIZE=1
RUN adduser --disabled-password --gecos "" superjack_user
USER superjack_user

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]