
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TZ=Asia/Kolkata

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port (from info.py)
EXPOSE 8080

# Run Command 
CMD ["python", "ftm.py"]
