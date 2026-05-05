FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install minimal system deps (psycopg2 requires libpq-dev)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         gcc g++ build-essential cmake pkg-config \
         libpq-dev libssl-dev libffi-dev \
         libopenblas-dev liblapack-dev \
         libjpeg-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.docker.txt ./

RUN python -m pip install --upgrade pip
# Use docker-specific requirements if present and non-empty, otherwise fall back to requirements.txt
RUN /bin/sh -c "if [ -f requirements.docker.txt ] && [ -s requirements.docker.txt ]; then pip install --no-cache-dir -r requirements.docker.txt; else pip install --no-cache-dir -r requirements.txt; fi"

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["python", "run.py"]
