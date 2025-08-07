# Cursor Rules for 16TypeDatabaseCN

This directory contains Cursor rules that help maintain code quality, consistency, and prevent common issues in the 16TypeDatabaseCN project.

## Available Rules

### 1. [Emoji Usage](./emoji-usage.md)
Prevents emoji usage in code files to avoid CI/CD pipeline failures and compatibility issues.

### 2. [CI/CD Standards](./ci-cd-standards.md)
Ensures proper CI/CD implementation patterns and prevents common pipeline failures.

### 3. [Code Quality](./code-quality.md)
Maintains high code quality standards using Black, Flake8, MyPy, and security tools.

### 4. [Project Structure](./project-structure.md)
Maintains consistent project organization and file naming conventions.

### 5. [Commit Messages](./commit-messages.md)
Ensures consistent commit message format for clear project history.

## How to Use

These rules are automatically applied by Cursor when you're working in this project. They will:

- Provide suggestions and warnings in the editor
- Help prevent common mistakes before they happen
- Ensure consistency across the development team
- Reduce CI/CD pipeline failures

## Rule Enforcement

The rules are enforced through:

1. Cursor Editor: Real-time suggestions and warnings
2. Pre-commit Hooks: Automated validation before commits
3. CI/CD Pipeline: Automated checks in GitHub Actions
4. Local CI Runner: Manual validation with `python run_local_ci.py`

## Adding New Rules

To add a new rule:

1. Create a new `.md` file in this directory
2. Follow the established format with Description, Examples, and Scope
3. Update this README to include the new rule
4. Test the rule locally before committing

## Rule Maintenance

Rules should be updated when:

- New tools or standards are adopted
- Common issues are identified
- Team feedback suggests improvements
- Project requirements change

## Related Documentation

- [DEVELOPMENT_GUIDELINES.md](../DEVELOPMENT_GUIDELINES.md)
- [CI_CD_RULES.md](../CI_CD_RULES.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [TODO.md](../TODO.md)
