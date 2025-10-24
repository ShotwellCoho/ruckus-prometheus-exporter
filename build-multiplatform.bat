@echo off
REM Multi-platform Docker build script for Ruckus AP Exporter (Windows)

echo 🏗️ Building Ruckus AP Exporter for multiple platforms...
echo Platforms: linux/amd64, linux/arm64

REM Enable Docker BuildKit
set DOCKER_BUILDKIT=1

REM Create and use a new builder instance for multi-platform builds
docker buildx create --name multiplatform-builder --use --bootstrap

REM Build for local use (loads native architecture)
echo Building for local architecture...
docker buildx build --platform linux/amd64,linux/arm64 --tag ruckus-exporter:latest --load .

REM Show available images
echo ✅ Build complete! Available images:
docker images | findstr ruckus-exporter

echo.
echo 🚀 Usage:
echo   Standard: docker-compose up -d
echo   Multi-platform: docker-compose -f docker-compose-multiplatform.yml up -d
echo.
echo 🔧 Manual platform selection:
echo   AMD64: docker run --platform linux/amd64 ruckus-exporter:latest
echo   ARM64: docker run --platform linux/arm64 ruckus-exporter:latest

pause