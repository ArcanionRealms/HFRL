#!/bin/bash

# HFRL Integration Hub - GitHub Push Script
# This script will push only the necessary files to GitHub

echo "🚀 HFRL Integration Hub - GitHub Push Helper"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Initializing..."
    git init
    echo "✅ Git initialized"
fi

# Add .gitignore first
echo "📝 Adding .gitignore..."
git add .gitignore

# Add only the files we want to push
echo "📝 Adding files to commit..."

# Frontend files
git add index.html
git add main.js
git add analytics.html
git add documentation.html
git add settings.html
git add design.md
git add interaction.md
git add outline.md

# Resources
git add resources/

# Documentation (only README.md)
git add README.md

# Backend files
git add backend/main.py
git add backend/requirements.txt
git add backend/run.sh
git add backend/QUICKSTART.md
git add backend/README.md
git add backend/.env.example
git add backend/.gitignore
git add backend/app/

echo ""
echo "📋 Files staged for commit:"
git status --short

echo ""
echo "⚠️  Files that will NOT be pushed (as per .gitignore):"
echo "   - QUICKSTART.md"
echo "   - IMPROVEMENTS.md"
echo "   - CONTRIBUTING.md"
echo "   - LICENSE"
echo "   - PRE-PUSH-CHECKLIST.md"
echo "   - .github-setup.md"
echo "   - .env files"
echo "   - __pycache__ directories"
echo "   - venv/ directory"
echo ""

read -p "📝 Enter commit message (or press Enter for default): " commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="feat: initial commit with HFRL platform

- Frontend with responsive UI
- FastAPI backend with professional practices
- Multi-provider AI integration
- Feedback and analytics system
- Complete documentation"
fi

echo ""
echo "💾 Creating commit..."
git commit -m "$commit_msg"

echo ""
echo "🔗 Repository Setup:"
echo "   1. Create a new repository on GitHub"
echo "   2. Copy the repository URL"
echo ""
read -p "📎 Enter your GitHub repository URL: " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ No URL provided. Skipping remote setup."
    echo "   You can add it later with:"
    echo "   git remote add origin YOUR_REPO_URL"
    echo "   git push -u origin main"
    exit 0
fi

# Add remote
echo "🔗 Adding remote..."
git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"

# Set branch to main
echo "🌿 Setting branch to main..."
git branch -M main

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🎉 Next steps:"
echo "   1. Visit your repository on GitHub"
echo "   2. Add repository description and topics"
echo "   3. Configure repository settings"
echo "   4. Share your project!"
echo ""
