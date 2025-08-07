# Emoji Usage Rule

## Description
Never use emojis in Python code files, comments, or string literals. Emojis can cause compatibility issues in different terminal environments and CI/CD pipelines.

## Examples

### INCORRECT
```python
print("SUCCESS: Success!")  # Emoji in string
# STARTING: Starting the application  # Emoji in comment
return "COMPLETED: Operation completed"  # Emoji in return value
```

### CORRECT
```python
print("SUCCESS: Operation completed")  # Text prefix
# STARTING: Application initialization  # Text prefix in comment
return "Operation completed successfully"  # Plain text
```

## Rationale
- Terminal compatibility issues
- CI/CD pipeline failures
- Log parsing difficulties
- Cross-platform consistency
- Accessibility concerns

## Scope
- All Python files (`.py`)
- All comments and docstrings
- All string literals
- All print statements
