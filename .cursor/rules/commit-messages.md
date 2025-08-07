# Commit Message Standards Rule

## Description
Use consistent commit message format to maintain clear project history and enable automated changelog generation.

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies, etc.
- `ci`: CI/CD changes
- `perf`: Performance improvements
- `build`: Build system changes

### Scopes
- `auth`: Authentication related
- `api`: API endpoints
- `db`: Database related
- `ui`: User interface
- `ci`: CI/CD pipeline
- `docs`: Documentation
- `deps`: Dependencies

## Examples

### CORRECT
```
feat(auth): add JWT token refresh endpoint

- Add /auth/refresh endpoint for token renewal
- Implement refresh token validation
- Add refresh token to user model

Closes #123
```

```
fix(ci): resolve safety command syntax error

Update safety command from --output to --output-file
to fix CI pipeline failures.

Fixes #456
```

```
docs(api): update API documentation

- Add missing endpoint descriptions
- Include request/response examples
- Update OpenAPI schema
```

```
style: format code with Black

Run black formatter on all Python files to ensure
consistent code formatting.
```

### INCORRECT
```
fixed bug  # Too vague
```

```
updated stuff  # No type, no scope, unclear
```

```
feat: add new feature  # Missing scope
```

```
FIX: broken thing  # Wrong type format
```

## Guidelines

### 1. Description
- Use imperative mood ("add" not "added")
- Keep under 72 characters
- Start with lowercase letter
- No period at the end

### 2. Body
- Explain what and why, not how
- Wrap at 72 characters
- Use bullet points for multiple changes

### 3. Footer
- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`

### 4. Scope
- Use lowercase
- Keep it short and specific
- Use existing scopes when possible

## Automation

### Pre-commit Hook
The project uses pre-commit hooks to validate commit messages:
- Check format compliance
- Ensure type and scope are valid
- Verify description length

### Changelog Generation
Commit messages are used to automatically generate:
- CHANGELOG.md updates
- Release notes
- GitHub release descriptions

## Scope
- All commit messages
- All branch names
- All pull request titles
- All release notes
