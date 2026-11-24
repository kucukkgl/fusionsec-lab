FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app --home-dir /app app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .
RUN mkdir -p logs dfir_artifacts \
    && chown -R app:app /app

USER app

EXPOSE 80

CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "80"]
