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

COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY entrypoint.sh /app/entrypoint.sh

RUN mkdir -p /server/src/logs

RUN mkdir -p /server/src/temp

COPY src /app/server/src

# Change ownership of the application directory
RUN chown -R appuser:appuser /app /server

USER root

USER appuser

RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
