@echo off
REM GitHub Repository Setup Script for Ruckus AP Exporter (Windows)

echo 🚀 Setting up GitHub repository for Ruckus AP Exporter
echo ==================================================

REM Check if git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git and try again.
    pause
    exit /b 1
)

REM Initialize git repository if not already done
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

REM Create .gitignore if it doesn't exist
if not exist ".gitignore" (
    echo 📝 Creating .gitignore...
    (
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo pip-wheel-metadata/
echo share/python-wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo MANIFEST
echo.
echo # Virtual environments
echo .env
echo .venv
echo env/
echo venv/
echo ENV/
echo env.bak/
echo venv.bak/
echo.
echo # IDEs
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo .DS_Store?
echo ._*
echo .Spotlight-V100
echo .Trashes
echo ehthumbs.db
echo Thumbs.db
echo.
echo # Docker
echo .dockerignore
echo.
echo # Logs
echo *.log
echo logs/
echo.
echo # Environment files
echo .env.local
echo .env.production
echo.
echo # Temporary files
echo *.tmp
echo *.bak
    ) > .gitignore
    echo ✅ .gitignore created
)

REM Add all files to git
echo 📋 Adding files to git...
git add .

REM Create initial commit if no commits exist
git rev-parse --verify HEAD >nul 2>&1
if %errorlevel% neq 0 (
    echo 💾 Creating initial commit...
    git commit -m "Initial commit: Ruckus AP Metrics Exporter" -m "" -m "- Multi-platform Docker support (x86_64 and ARM64)" -m "- Multi-AP SNMP monitoring capability" -m "- Prometheus metrics export with proper labeling" -m "- GitHub Actions CI/CD pipeline" -m "- Comprehensive documentation and security policies" -m "- Production-ready configuration"
    echo ✅ Initial commit created
) else (
    echo ✅ Repository already has commits
)

echo.
echo 🎯 Next Steps:
echo ==============
echo.
echo 1. 📂 Create GitHub Repository:
echo    - Go to https://github.com/new
echo    - Repository name: RuckusExporter
echo    - Description: Prometheus exporter for Ruckus Wireless Access Points with multi-platform Docker support
echo    - Make it Public
echo    - Don't initialize with README (we already have one)
echo.
echo 2. 🔗 Add GitHub remote (replace 'yourusername' with your GitHub username):
echo    git remote add origin https://github.com/yourusername/RuckusExporter.git
echo.
echo 3. 📤 Push to GitHub:
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. 🐳 Set up Docker Hub:
echo    - Go to https://hub.docker.com/repository/create
echo    - Repository name: ruckus-ap-exporter
echo    - Description: Multi-platform Prometheus exporter for Ruckus APs
echo    - Make it Public
echo.
echo 5. 🔑 Add GitHub Secrets:
echo    Go to: https://github.com/yourusername/RuckusExporter/settings/secrets/actions
echo    Add these secrets:
echo    - DOCKERHUB_USERNAME: your Docker Hub username
echo    - DOCKERHUB_TOKEN: your Docker Hub access token
echo.
echo 6. 📝 Update README badges:
echo    Replace 'yourusername' in README.md with your actual GitHub/Docker Hub username
echo.
echo 7. 🏷️ Create first release:
echo    - Go to https://github.com/yourusername/RuckusExporter/releases/new
echo    - Tag: v1.0.0
echo    - Title: v1.0.0 - Initial Release
echo    - Description: Copy from CHANGELOG.md
echo.
echo 🎉 After these steps, your repository will have:
echo    ✅ Automatic Docker builds for x86_64 and ARM64
echo    ✅ Public Docker Hub images
echo    ✅ CI/CD pipeline with tests
echo    ✅ Professional documentation
echo    ✅ Security policies and contribution guidelines
echo.
echo Ready to make your project public! 🚀

pause