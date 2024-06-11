FROM python:3.12

LABEL authors="Ashish Pal"
LABEL version="1.0.0"

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    tesseract-ocr-mar \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application files
COPY entrypoint.sh /app/entrypoint.sh
COPY src /app/server/src

# Create directories and set permissions
RUN mkdir -p /app/server/src/logs /app/temp \
    && chown -R appuser:appuser /app /app/temp

# Switch to the non-root user
USER appuser

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
