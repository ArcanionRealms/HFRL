# Contributing to Arcanion HFRL

Thank you for your interest in contributing! This document outlines how to participate in the project.

## License & Legal Requirements

### Business Source License Compliance
This project is licensed under the **Business Source License 1.1**. By contributing, you agree:

1. **Copyright Assignment**: You must sign a Contributor License Agreement (CLA) assigning copyright to Arcanion. This is required for dual licensing.
   - [Click here to sign CLA]([LINK TO CLA FORM])

2. **License Headers**: All source files must include the Business Source License header.
   - The pre-commit hook will automatically check this
   - If you add new files, run: `./add-license.sh`

3. **No Open Core**: Free and commercial versions must have **identical source code**. Do not attempt to create separate proprietary features.

### What "Commercial Use" Means
You may NOT contribute features specifically for commercial-only use. All features must be available to the entire community.

## How to Contribute

### Reporting Issues
- **Bugs**: Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- **Feature Requests**: Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- **Security Issues**: Email arcanion.realms@gmail.com or contact garimitsu on Discord directly (do NOT use public issues)

### Pull Request Process

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/repo-name.git`
3. **Create a feature branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes**
5. **Add tests** for new functionality
6. **Ensure license headers** are present on all new files
7. **Run tests**: `npm test` or `pytest` or equivalent
8. **Commit** with clear messages: `git commit -m "Add user authentication module"`
9. **Push** to your fork: `git push origin feature/your-feature-name`
10. **Create Pull Request** against our `main` branch

### PR Requirements
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] All new files have BSL headers
- [ ] CLA is signed
- [ ] PR description includes "Fixes #issue-number" if applicable
- [ ] Documentation updated if needed

## Development Setup

```bash
# Clone repository
git clone https://github.com/[USERNAME]/[REPO].git
cd [REPO]

# Install dependencies
# Add your specific setup commands here

# Run tests
# Add your test command here

# Install pre-commit hook (required)
ln -s -f ../../.github/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
