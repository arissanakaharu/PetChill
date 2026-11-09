FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLET_FORCE_WEB_SERVER=true
ENV FLET_SERVER_IP=0.0.0.0
ENV FLET_SERVER_PORT=8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]