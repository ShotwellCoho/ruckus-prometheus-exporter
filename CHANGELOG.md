# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Multi-platform Docker support (x86_64 and ARM64)
- Multi-AP monitoring capability
- GitHub Actions CI/CD pipeline
- Docker Hub automated builds
- Comprehensive documentation
- Security policy and contributing guidelines

## [1.0.0] - 2025-10-24

### Added
- Initial release of Ruckus AP Metrics Exporter
- SNMP v2c monitoring for Ruckus Access Points
- Prometheus metrics export with proper labeling
- Docker containerization with ARM64 support
- System metrics collection (uptime, info)
- Interface metrics collection (status, bytes, packets)
- Wireless client monitoring
- Health check endpoints
- Configurable environment variables
- Multi-AP support via comma-separated host list
- Error handling and logging
- Performance monitoring (scrape duration)
- Docker Compose configuration
- Build scripts for multi-platform deployment

### Technical Details
- Python 3.11 base image
- pysnmp for SNMP communication
- prometheus-client for metrics export
- Non-root container execution for security
- Comprehensive SNMP OID mapping for Ruckus devices

### Supported Platforms
- linux/amd64 (x86_64)
- linux/arm64 (ARM64)

### Dependencies
- prometheus-client==0.20.0
- pysnmp==4.4.12
- pyasn1==0.4.8