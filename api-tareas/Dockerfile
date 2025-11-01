FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN useradd -m -u 10001 appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p /app/data && chown -R appuser:appuser /app
USER appuser

ENV PORT=5000 \
    FLASK_ENV=production \
    DATABASE_URL=sqlite:////app/data/tasks.db

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-k", "gthread", "-t", "120", "-b", "0.0.0.0:5000", "app:app"]
