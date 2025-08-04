# Task ID System & Branching Strategy Guide

## Overview
This project uses a systematic approach to task management with unique IDs and consistent branch naming conventions.

## Task ID System

### Format
- **TASK-001** to **TASK-999** for sequential task numbering
- **TASK-1000+** for future tasks
- All task IDs are padded with leading zeros (e.g., TASK-008, TASK-015)

### Current Task Status
- **TASK-001** to **TASK-007**: ✅ **COMPLETED**
- **TASK-008**: 🔄 **NEXT PRIORITY** (Voting endpoints)
- **TASK-009**: 📋 **PENDING** (Comment endpoints)
- **TASK-010+**: 📋 **PENDING**

## Branch Naming Convention

### Branch Types
- **Feature branches**: `feature/TASK-XXX-description`
- **Bug fixes**: `fix/TASK-XXX-description`
- **Hotfixes**: `hotfix/TASK-XXX-description`
- **Documentation**: `docs/TASK-XXX-description`

### Examples
- `feature/TASK-008-voting-endpoints`
- `fix/TASK-012-auth-bug`
- `docs/TASK-015-api-documentation`
- `hotfix/TASK-020-security-patch`

## How to Create a New Task Branch

### Option 1: Using the Batch Script (Windows)
```cmd
create_task_branch.bat 008 feature voting-endpoints
```

### Option 2: Using the PowerShell Script
```powershell
.\create_task_branch.ps1 -TaskId "008" -Type "feature" -Description "voting-endpoints"
```

### Option 3: Manual Git Commands
```bash
# Make sure you're on main branch
git checkout main
git pull origin main

# Create and switch to new branch
git checkout -b feature/TASK-008-voting-endpoints

# Start working on your task
# ... make your changes ...

# Commit your changes
git add .
git commit -m "TASK-008: Implement voting endpoints"

# Push the branch
git push origin feature/TASK-008-voting-endpoints
```

## Workflow for Each Task

### 1. Start a New Task
```bash
# Create new branch from main
create_task_branch.bat [TaskId] [Type] [Description]
```

### 2. Work on the Task
- Make your changes
- Test your implementation
- Update TODO.md to mark progress

### 3. Commit Your Changes
```bash
git add .
git commit -m "TASK-XXX: [Description of changes]"
```

### 4. Push and Create Pull Request
```bash
git push origin [branch-name]
# Then create PR on GitHub
```

### 5. After Merge
```bash
# Switch back to main
git checkout main
git pull origin main

# Delete the feature branch
git branch -d [branch-name]
```

## Commit Message Format

### Standard Format
```
TASK-XXX: Brief description of changes

Optional: More detailed explanation if needed
```

### Examples
```
TASK-008: Implement voting endpoints

- Add POST /votes endpoint
- Add GET /votes endpoint
- Add vote validation logic
- Add daily vote limits
```

## Task Status Tracking

### Status Indicators
- ✅ **COMPLETED** - Task is finished and merged
- 🔄 **IN PROGRESS** - Currently being worked on
- 📋 **PENDING** - Planned but not started
- ⭐ **PRIORITY** - High priority task

### Updating Task Status
1. Update TODO.md with current progress
2. Use appropriate status indicators
3. Add completion dates when tasks are finished

## Best Practices

### 1. Always Start from Main
- Ensure you're on the latest main branch before creating new branches
- Pull latest changes: `git pull origin main`

### 2. Keep Branches Focused
- One task per branch
- Keep changes related to the specific task
- Don't mix multiple tasks in one branch

### 3. Regular Commits
- Commit frequently with descriptive messages
- Use the TASK-XXX format in commit messages
- Include the task ID in all related commits

### 4. Update Documentation
- Update TODO.md as you progress
- Mark tasks as completed when done
- Add any new tasks that are discovered

### 5. Clean Up After Merge
- Delete feature branches after successful merge
- Keep main branch clean and up to date

## Current Priority Tasks

### Immediate Next Steps
1. **TASK-008**: Implement voting system endpoints 🔄 **NEXT PRIORITY**
2. **TASK-009**: Create comment system endpoints 📋 **PENDING**
3. **TASK-010**: Add search functionality 📋 **PENDING**

### How to Start TASK-008
```bash
# Create branch for voting endpoints
create_task_branch.bat 008 feature voting-endpoints

# This will create: feature/TASK-008-voting-endpoints
# You'll be automatically switched to this branch
# Start implementing the voting system endpoints
```

## Troubleshooting

### Common Issues
1. **Branch already exists**: Delete the old branch first
2. **Not on main branch**: Switch to main before creating new branch
3. **Merge conflicts**: Resolve conflicts before continuing

### Useful Commands
```bash
# Check current branch
git branch --show-current

# List all branches
git branch -a

# Switch to main
git checkout main

# Delete local branch
git branch -d [branch-name]

# Delete remote branch
git push origin --delete [branch-name]
```

## Integration with GitHub

### Pull Request Naming
- Use the same format: `TASK-XXX: [Description]`
- Example: `TASK-008: Implement voting endpoints`

### Pull Request Description
```
## Task ID
TASK-008

## Description
Implement voting system endpoints for the MBTI roster application.

## Changes Made
- Added POST /votes endpoint
- Added GET /votes endpoint
- Implemented vote validation
- Added daily vote limits

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing completed

## Related Issues
Closes #[issue-number]
```

This system ensures consistent task tracking, clear branch management, and professional development workflow. 