FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for OpenCV and scientific stack
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

EXPOSE 5000

# You can switch to gunicorn + eventlet for production:
# CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
CMD ["python", "app.py"]
