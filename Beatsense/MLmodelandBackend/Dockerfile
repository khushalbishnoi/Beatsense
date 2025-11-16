# backend Dockerfile
FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates wget && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r beatsense && useradd --no-log-init -r -g beatsense beatsense \
    && chown -R beatsense:beatsense /app
USER beatsense

LABEL maintainer="Your Name <you@example.com>"
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD wget -qO- http://localhost:5000/health || exit 1

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]
