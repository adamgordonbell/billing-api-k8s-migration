# syntax=docker/dockerfile:1.7

# Build stage — compile any deps that need a compiler.
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage — slim, non-root.
FROM python:3.12-slim
RUN groupadd -g 10001 appuser \
 && useradd -u 10001 -g 10001 -s /usr/sbin/nologin -M appuser

COPY --from=build /install /usr/local
WORKDIR /app
COPY src/ ./src/

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PORT=8080

USER appuser
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "billing_api.app:app"]
