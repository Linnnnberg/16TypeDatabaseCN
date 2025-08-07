# Git Ignore Strategy Guide

This document explains the Git ignore rules and strategy for the 16TypeDatabaseCN project.

## Overview

Our Git ignore strategy ensures that:
- Sensitive files are never committed
- Generated files are excluded
- Development artifacts are ignored
- Team collaboration files are preserved

## Main .gitignore Categories

### 1. Python Development
```
# Python bytecode and cache
__pycache__/
*.py[cod]
*.so

# Virtual environments
venv/
env/
.venv/

# Python packaging
build/
dist/
*.egg-info/
```

### 2. Environment and Configuration
```
# Environment variables (sensitive)
.env
.env.local
.env.production
.env.development
.env.test

# Local configuration
local_settings.py
local_config.py
```

### 3. Database Files
```
# SQLite databases
*.db
*.sqlite3
*.sqlite
mbti_roster.db
test_mbti_roster.db
```

### 4. IDE and Editor Files
```
# VS Code
.vscode/

# PyCharm/IntelliJ
.idea/

# Vim
*.swp
*.swo
*~

# Cursor (with exceptions for rules)
.cursor/
```

### 5. Testing and Coverage
```
# Coverage reports
htmlcov/
.coverage
coverage.xml
*.cover

# Test cache
.pytest_cache/
.tox/
.hypothesis/
```

### 6. Security and Dependency Reports
```
# Security scan reports
bandit-report.json
safety-report.json
*.sarif
```

### 7. Generated Documentation
```
# API documentation (generated)
docs/app/
docs/api/
```

### 8. Data Processing
```
# Processed data files
data_uploads/processed/
data_uploads/failed/
```

## Cursor Rules Strategy

### What's Ignored
- `.cursor/` directory (IDE-specific files)
- Cursor cache and temporary files
- User-specific settings

### What's Tracked
- `.cursor/rules/` directory (team collaboration)
- All `.md` files in rules directory
- Rule documentation and examples

### Rationale
- Cursor rules are valuable for team collaboration
- IDE-specific files should not be shared
- Rules help maintain code quality across the team

## Environment Variables Strategy

### Never Committed
- `.env` files (contain sensitive data)
- Local configuration files
- Production secrets

### Always Committed
- `.env.example` (template)
- Configuration documentation
- Default settings in code

## Database Strategy

### Never Committed
- Actual database files (`.db`, `.sqlite3`)
- Database backups
- Test databases

### Always Committed
- Database schemas (migrations)
- Seed data scripts
- Database documentation

## Security Considerations

### Files Never Committed
```
# Secrets and keys
*.key
*.pem
*.p12
*.pfx

# API keys and tokens
secrets.json
config.json (if contains secrets)

# Database credentials
database.ini
db_config.py
```

### Files Always Committed
```
# Templates and examples
config.example.json
database.example.ini
.env.example
```

## Best Practices

### 1. Check Before Committing
```bash
# See what will be committed
git status

# See ignored files
git status --ignored

# Check specific file
git check-ignore filename
```

### 2. Test Ignore Rules
```bash
# Test if a file is ignored
git check-ignore path/to/file

# Test multiple files
git check-ignore file1 file2 file3
```

### 3. Update Ignore Rules
- Add new patterns when needed
- Document changes in this guide
- Test with team members

### 4. Handle Sensitive Files
```bash
# Remove sensitive file from tracking
git rm --cached sensitive_file.txt

# Update .gitignore
echo "sensitive_file.txt" >> .gitignore

# Commit the change
git add .gitignore
git commit -m "chore: ignore sensitive file"
```

## Common Scenarios

### Scenario 1: Adding New Environment Variables
1. Update `.env.example` with new variable (no value)
2. Add to documentation
3. Never commit actual `.env` file

### Scenario 2: Generated Files
1. Add pattern to `.gitignore`
2. Remove from tracking: `git rm --cached file`
3. Commit the change

### Scenario 3: IDE Files
1. Add IDE pattern to `.gitignore`
2. Remove existing files: `git rm -r --cached .vscode/`
3. Commit the change

## Troubleshooting

### File Still Tracked After Adding to .gitignore
```bash
# Remove from tracking (keeps local file)
git rm --cached filename

# Commit the change
git add .gitignore
git commit -m "chore: stop tracking filename"
```

### Check What's Ignored
```bash
# List all ignored files
git status --ignored

# Check specific file
git check-ignore path/to/file
```

### Global vs Local Ignore
- Use `.gitignore` for project-specific rules
- Use `~/.gitignore_global` for personal rules
- Configure: `git config --global core.excludesfile ~/.gitignore_global`

## Maintenance

### Regular Tasks
1. Review ignored files monthly
2. Update patterns for new tools
3. Clean up unnecessary patterns
4. Document changes

### Team Coordination
1. Discuss ignore rule changes
2. Test with different environments
3. Update documentation
4. Notify team of changes

## Related Files

- `.gitignore` - Main ignore rules
- `.cursor/.gitignore` - Cursor-specific rules
- `DEVELOPMENT_GUIDELINES.md` - Development standards
- `CI_CD_RULES.md` - CI/CD guidelines
