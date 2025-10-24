#!/bin/bash
# GitHub Repository Setup Script for Ruckus AP Exporter

set -e

echo "🚀 Setting up GitHub repository for Ruckus AP Exporter"
echo "=================================================="

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git and try again."
    exit 1
fi

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Docker
.dockerignore

# Logs
*.log
logs/

# Environment files
.env.local
.env.production

# Temporary files
*.tmp
*.bak
EOF
    echo "✅ .gitignore created"
fi

# Add all files to git
echo "📋 Adding files to git..."
git add .

# Create initial commit if no commits exist
if ! git rev-parse --verify HEAD &> /dev/null; then
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: Ruckus AP Metrics Exporter

- Multi-platform Docker support (x86_64 and ARM64)
- Multi-AP SNMP monitoring capability  
- Prometheus metrics export with proper labeling
- GitHub Actions CI/CD pipeline
- Comprehensive documentation and security policies
- Production-ready configuration"
    echo "✅ Initial commit created"
else
    echo "✅ Repository already has commits"
fi

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. 📂 Create GitHub Repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: RuckusExporter"
echo "   - Description: Prometheus exporter for Ruckus Wireless Access Points with multi-platform Docker support"
echo "   - Make it Public"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "2. 🔗 Add GitHub remote (replace 'yourusername' with your GitHub username):"
echo "   git remote add origin https://github.com/yourusername/RuckusExporter.git"
echo ""
echo "3. 📤 Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. 🐳 Set up Docker Hub:"
echo "   - Go to https://hub.docker.com/repository/create"
echo "   - Repository name: ruckus-ap-exporter"
echo "   - Description: Multi-platform Prometheus exporter for Ruckus APs"
echo "   - Make it Public"
echo ""
echo "5. 🔑 Add GitHub Secrets:"
echo "   Go to: https://github.com/yourusername/RuckusExporter/settings/secrets/actions"
echo "   Add these secrets:"
echo "   - DOCKERHUB_USERNAME: your Docker Hub username"
echo "   - DOCKERHUB_TOKEN: your Docker Hub access token"
echo ""
echo "6. 📝 Update README badges:"
echo "   Replace 'yourusername' in README.md with your actual GitHub/Docker Hub username"
echo ""
echo "7. 🏷️ Create first release:"
echo "   - Go to https://github.com/yourusername/RuckusExporter/releases/new"
echo "   - Tag: v1.0.0"
echo "   - Title: v1.0.0 - Initial Release"
echo "   - Description: Copy from CHANGELOG.md"
echo ""
echo "🎉 After these steps, your repository will have:"
echo "   ✅ Automatic Docker builds for x86_64 and ARM64"
echo "   ✅ Public Docker Hub images"
echo "   ✅ CI/CD pipeline with tests"
echo "   ✅ Professional documentation"
echo "   ✅ Security policies and contribution guidelines"
echo ""
echo "Ready to make your project public! 🚀"