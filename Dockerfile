# -------- Stage 1: builder (compile wheels, install deps) --------
FROM python:3.13-slim AS builder

ARG POETRY=false
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

# system deps for building wheels (add any libs you need, e.g. libpq-dev, gcc)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    curl \
    libpq-dev \
    libffi-dev \
    libsasl2-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt requirements-dev.txt /app/

# Use a wheelhouse dir to cache wheels between builds (optional)
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip wheel --wheel-dir /wheels -r requirements.txt

# -------- Stage 2: runtime image --------
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# create non-root user
ARG APP_USER=app
ARG APP_UID=1000
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ca-certificates \
    build-essential \
    libjpeg62-turbo-dev \
 && rm -rf /var/lib/apt/lists/* \
 && groupadd -g ${APP_UID} ${APP_USER} || true \
 && useradd -u ${APP_UID} -g ${APP_USER} -m -s /bin/bash ${APP_USER}

WORKDIR /app

# Copy wheelhouse from builder, install
COPY --from=builder /wheels /wheels
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir -r requirements.txt --find-links /wheels \
 && rm -rf /wheels

COPY . /app
# Ensure migrations / manage.py are executable (if needed)
RUN chown -R ${APP_USER}:${APP_USER} /app

# Path for collectstatic and logs
ENV STATIC_ROOT=/app/staticfiles \
    MEDIA_ROOT=/app/media

# Entrypoint & gunicorn settings
COPY docker/entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

USER ${APP_USER}

# Expose port (Gunicorn)
EXPOSE 8000

# Default command for web service (overridden in compose for worker/beat)
CMD ["/app/docker-entrypoint.sh", "gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
