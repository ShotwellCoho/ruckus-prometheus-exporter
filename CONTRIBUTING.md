# Contributing to Ruckus AP Exporter

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed and what behavior you expected
* Include details about your configuration and environment

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the enhancement
* Describe the current behavior and explain the behavior you expected to see
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guides
* Include thoughtfully-worded, well-structured tests
* Document new code based on the Documentation Styleguide
* End all files with a newline

## Development Setup

### Prerequisites

* Python 3.10+
* Docker and Docker Compose
* Access to Ruckus AP for testing

### Local Development

1. Fork and clone the repository
```bash
git clone https://github.com/yourusername/RuckusExporter.git
cd RuckusExporter
```

2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
export RUCKUS_AP_HOSTS="192.168.1.100"
export SNMP_COMMUNITY="public"
```

5. Run the exporter
```bash
python ruckus_exporter.py
```

### Testing

Run the diagnostic script to test SNMP connectivity:
```bash
python snmp_diagnostic.py
```

Test the metrics endpoint:
```bash
curl http://localhost:8000/metrics
```

### Docker Development

Build and test locally:
```bash
docker build -t ruckus-exporter:dev .
docker run -p 8000:8000 -e RUCKUS_AP_HOSTS="192.168.1.100" ruckus-exporter:dev
```

Test multi-platform builds:
```bash
./build-multiplatform.sh  # Linux/macOS
# or
build-multiplatform.bat   # Windows
```

## Style Guide

### Python Code Style

* Follow PEP 8
* Use type hints where appropriate
* Write descriptive docstrings for functions and classes
* Keep functions focused and small
* Use meaningful variable and function names

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Example:
```
Add support for Ruckus R750 AP model

- Implement new SNMP OIDs for R750 specific metrics
- Update interface discovery logic
- Add tests for R750 model detection
- Update documentation

Fixes #123
```

## Documentation

* Update README.md for any user-facing changes
* Update inline code documentation
* Add examples for new features
* Update Docker Hub description via GitHub Actions

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create a pull request
4. After merge, create a git tag
5. GitHub Actions will automatically build and publish Docker images

## Questions?

Feel free to open an issue for any questions about contributing!