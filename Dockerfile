# Use Python 3.11 slim image with ARM64 support
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ruckus_exporter.py .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash exporter
USER exporter

# Expose metrics port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000')" || exit 1

# Set default environment variables
ENV RUCKUS_AP_HOST=192.168.1.100
ENV SNMP_COMMUNITY=public
ENV SNMP_PORT=161
# For multiple APs, set RUCKUS_AP_HOSTS instead: "192.168.1.100,192.168.1.101,192.168.1.102"
ENV METRICS_PORT=8000
ENV SCRAPE_INTERVAL=30

# Run the exporter
CMD ["python", "ruckus_exporter.py"]