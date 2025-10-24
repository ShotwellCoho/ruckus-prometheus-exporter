# Multi-Platform Docker Deployment Guide

## Platform Compatibility ✅

The Ruckus AP Exporter Docker container is now compatible with:
- **x86_64 (AMD64)**: Intel/AMD processors - Standard desktop, server, cloud instances
- **ARM64**: ARM processors - Raspberry Pi, Apple M1/M2, ARM cloud instances, IoT devices

## Deployment Methods

### Method 1: Automatic Platform Detection (Recommended)
The simplest approach - Docker automatically uses your native architecture:

```bash
# Clone repository
git clone <your-repo>
cd RuckusExporter

# Start with auto-detection
docker-compose up -d
```

### Method 2: Multi-Platform Build
For advanced users who want to build for multiple architectures:

```bash
# Enable BuildKit and create multi-platform builder
export DOCKER_BUILDKIT=1
docker buildx create --name multiplatform-builder --use --bootstrap

# Build for both platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ruckus-exporter:multiplatform \
  --load .

# Run the multi-platform compose
docker-compose -f docker-compose-multiplatform.yml up -d
```

### Method 3: Manual Platform Selection
Explicitly specify the architecture:

```bash
# For x86_64 systems
docker run --platform linux/amd64 -d \
  --name ruckus-exporter-amd64 \
  -p 8000:8000 \
  -e RUCKUS_AP_HOSTS=192.168.1.100,192.168.1.101 \
  ruckus-exporter:latest

# For ARM64 systems  
docker run --platform linux/arm64 -d \
  --name ruckus-exporter-arm64 \
  -p 8000:8000 \
  -e RUCKUS_AP_HOSTS=192.168.1.100,192.168.1.101 \
  ruckus-exporter:latest
```

## Platform-Specific Examples

### Raspberry Pi (ARM64)
```bash
# Verify architecture
uname -m  # Should show: aarch64

# Deploy (auto-detects ARM64)
docker-compose up -d

# Verify container architecture
docker exec ruckus-ap-exporter uname -m
```

### x86_64 Desktop/Server
```bash
# Verify architecture  
uname -m  # Should show: x86_64

# Deploy (auto-detects AMD64)
docker-compose up -d

# Verify container architecture
docker exec ruckus-ap-exporter uname -m
```

### Mixed Environment Deployment
If you have both x86_64 and ARM64 systems:

```bash
# Build once for both platforms
docker buildx build --platform linux/amd64,linux/arm64 -t ruckus-exporter:universal .

# Push to registry (optional)
docker buildx build --platform linux/amd64,linux/arm64 -t your-registry/ruckus-exporter:latest --push .

# Deploy on any architecture
docker-compose up -d
```

## Verification Commands

### Check Host Architecture
```bash
# Linux/macOS
uname -m

# Windows PowerShell
$env:PROCESSOR_ARCHITECTURE

# Docker system info
docker system info | grep Architecture
```

### Verify Container Architecture
```bash
# Check what platform the container is running
docker exec ruckus-ap-exporter uname -m

# Check available platforms for image
docker buildx imagetools inspect ruckus-exporter:latest
```

### Performance Testing
```bash
# Monitor resource usage
docker stats ruckus-ap-exporter

# Check metrics collection performance
curl http://localhost:8000/metrics | grep ruckus_scrape_duration_seconds
```

## Troubleshooting

### Platform Mismatch
If you see warnings about platform mismatches:
```bash
# Force rebuild for your platform
docker-compose build --no-cache

# Or specify platform explicitly
docker-compose up -d --force-recreate
```

### BuildKit Issues
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Reset builder
docker buildx rm multiplatform-builder
docker buildx create --name multiplatform-builder --use --bootstrap
```

### Registry Deployment
For production deployments across multiple architectures:

```bash
# Tag and push multi-platform image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag your-registry.com/ruckus-exporter:latest \
  --push .

# Update docker-compose.yml
# image: your-registry.com/ruckus-exporter:latest
```

## File Summary
- `Dockerfile`: Base configuration (platform-agnostic)
- `docker-compose.yml`: Standard deployment (auto-detects platform)
- `docker-compose-multiplatform.yml`: Advanced multi-platform configuration
- `build-multiplatform.sh`: Linux/macOS build script
- `build-multiplatform.bat`: Windows build script

## Benefits
✅ **Universal Compatibility**: Single codebase runs on any architecture  
✅ **Performance Optimized**: Native binaries for each platform  
✅ **Easy Deployment**: Simple docker-compose commands work everywhere  
✅ **Production Ready**: Supports enterprise mixed-architecture environments