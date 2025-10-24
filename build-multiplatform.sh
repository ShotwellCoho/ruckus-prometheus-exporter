#!/bin/bash
# Multi-platform Docker build script for Ruckus AP Exporter

# Enable Docker BuildKit for multi-platform builds
export DOCKER_BUILDKIT=1

echo "🏗️  Building Ruckus AP Exporter for multiple platforms..."
echo "Platforms: linux/amd64, linux/arm64"

# Create and use a new builder instance for multi-platform builds
docker buildx create --name multiplatform-builder --use --bootstrap

# Build for multiple architectures and push to registry (optional)
# Uncomment and modify the registry URL if you want to push to a registry
# docker buildx build \
#   --platform linux/amd64,linux/arm64 \
#   --tag your-registry/ruckus-exporter:latest \
#   --push \
#   .

# Build for local use (loads only native architecture)
echo "Building for local architecture..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ruckus-exporter:latest \
  --load \
  .

# Show available images
echo "✅ Build complete! Available images:"
docker images | grep ruckus-exporter

# Instructions for manual platform selection
echo ""
echo "🚀 Usage:"
echo "  Standard: docker-compose up -d"
echo "  Multi-platform: docker-compose -f docker-compose-multiplatform.yml up -d"
echo ""
echo "📋 Platform Information:"
echo "  Your host: $(uname -m)"
docker version --format 'json' | grep -E '"Architecture"|"Os"' | head -2
echo ""
echo "🔧 Manual platform selection:"
echo "  AMD64: docker run --platform linux/amd64 ruckus-exporter:latest"
echo "  ARM64: docker run --platform linux/arm64 ruckus-exporter:latest"