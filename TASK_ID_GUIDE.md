# Task ID System & Branching Strategy Guide

## Overview
This project uses a systematic approach to task management with unique IDs and consistent branch naming conventions.

## Task ID System

### New Task ID Format (Updated)
Based on task type, use the following prefixes:

- **STORY-001** to **STORY-999**: New features and enhancements
- **FIX-001** to **FIX-999**: Bug fixes and issue resolutions  
- **TECH-001** to **TECH-999**: Technical improvements and infrastructure changes

### Task Type Classification

#### STORY- (Feature/Enhancement)
- New user-facing features
- UI/UX improvements
- New functionality
- Feature enhancements
- User experience improvements

**Examples:**
- STORY-006: Display 16 Type Codes with Chinese Names on Root Page
- STORY-007: Make MBTI Type Cards Clickable
- STORY-008: Create MBTI Type Description Pages

#### FIX- (Bug Fix/Issue Resolution)
- Bug fixes
- Error corrections
- Issue resolutions
- Security patches
- Performance fixes

**Examples:**
- FIX-001: Fix login button not responding
- FIX-002: Resolve database connection timeout
- FIX-003: Fix vote counting bug

#### TECH- (Technical Enhancement)
- Code refactoring
- Infrastructure improvements
- Dependency updates
- CI/CD improvements
- Documentation updates
- Testing improvements

**Examples:**
- TECH-001: Update GitHub Actions to v4
- TECH-002: Add comprehensive test coverage
- TECH-003: Refactor authentication service

### Legacy Task IDs
- **TASK-001** to **TASK-999**: Legacy format (deprecated)
- Existing completed tasks keep their original IDs
- New tasks use the new prefix system

### Current Task Status
- **TASK-001** to **TASK-007**: **COMPLETED** (Legacy format)
- **TASK-008**: **COMPLETED** (Legacy format)
- **FIX-001**: **COMPLETED** (Register/Login button fix)
- **TECH-001**: **COMPLETED** (GitHub Actions v4 update)
- **TECH-002**: **COMPLETED** (CI test fixes)

## Branch Naming Convention

### Updated Branch Types
- **Feature branches**: `feature/STORY-XXX-description`
- **Bug fixes**: `fix/FIX-XXX-description`
- **Technical improvements**: `tech/TECH-XXX-description`
- **Hotfixes**: `hotfix/FIX-XXX-description`
- **Documentation**: `docs/TECH-XXX-description`

### Examples
- `feature/STORY-001-user-profile-page`
- `fix/FIX-002-database-timeout`
- `tech/TECH-003-add-test-coverage`
- `hotfix/FIX-004-security-patch`
- `docs/TECH-005-api-documentation`

## How to Create a New Task Branch

### Option 1: Using the Batch Script (Windows)
```cmd
# For new features
create_task_branch.bat STORY-001 feature user-profile-page

# For bug fixes
create_task_branch.bat FIX-002 fix database-timeout

# For technical improvements
create_task_branch.bat TECH-003 tech add-test-coverage
```

### Option 2: Using the PowerShell Script
```powershell
# For new features
.\create_task_branch.ps1 -TaskId "STORY-001" -Type "feature" -Description "user-profile-page"

# For bug fixes
.\create_task_branch.ps1 -TaskId "FIX-002" -Type "fix" -Description "database-timeout"

# For technical improvements
.\create_task_branch.ps1 -TaskId "TECH-003" -Type "tech" -Description "add-test-coverage"
```

### Option 3: Manual Git Commands
```bash
# Make sure you're on main branch
git checkout main
git pull origin main

# Create and switch to new branch (example for feature)
git checkout -b feature/STORY-001-user-profile-page

# Create and switch to new branch (example for bug fix)
git checkout -b fix/FIX-002-database-timeout

# Create and switch to new branch (example for technical improvement)
git checkout -b tech/TECH-003-add-test-coverage

# Start working on your task
# ... make your changes ...

# Commit your changes
git add .
git commit -m "STORY-001: Add user profile page"
git commit -m "FIX-002: Fix database timeout issue"
git commit -m "TECH-003: Add comprehensive test coverage"

# Push the branch
git push origin feature/STORY-001-user-profile-page
git push origin fix/FIX-002-database-timeout
git push origin tech/TECH-003-add-test-coverage
```

## Workflow for Each Task

### 1. Start a New Task
```bash
# Determine task type and create appropriate branch
# For features: create_task_branch.bat STORY-XXX feature description
# For fixes: create_task_branch.bat FIX-XXX fix description  
# For tech: create_task_branch.bat TECH-XXX tech description
```

### 2. Work on the Task
- Make your changes
- Test your implementation
- Update TODO.md to mark progress

### 3. Commit Your Changes
```bash
git add .
git commit -m "STORY-XXX: [Description of changes]"
git commit -m "FIX-XXX: [Description of changes]"
git commit -m "TECH-XXX: [Description of changes]"
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

### Updated Standard Format
```
STORY-XXX: Brief description of changes
FIX-XXX: Brief description of changes
TECH-XXX: Brief description of changes

Optional: More detailed explanation if needed
```

### Examples
```
STORY-001: Add user profile page

- Add profile page UI components
- Implement profile data display
- Add profile editing functionality
- Add avatar upload feature
```

```
FIX-002: Fix database timeout issue

- Increase connection timeout settings
- Add connection pooling
- Implement retry logic for failed connections
- Add better error handling
```

```
TECH-003: Add comprehensive test coverage

- Add unit tests for all services
- Add integration tests for API endpoints
- Add pytest configuration
- Add coverage reporting
```

## Task Status Tracking

### Status Indicators
- **COMPLETED** - Task is finished and merged
- **IN PROGRESS** - Currently being worked on
- **PENDING** - Planned but not started
- **PRIORITY** - High priority task

### Updating Task Status
1. Update TODO.md with current progress
2. Use appropriate status indicators
3. Add completion dates when tasks are finished
4. Use correct task ID prefix (STORY-, FIX-, TECH-)

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
- Use the correct prefix format in commit messages (STORY-, FIX-, TECH-)
- Include the task ID in all related commits

### 4. Update Documentation
- Update TODO.md as you progress
- Mark tasks as completed when done
- Add any new tasks that are discovered
- Use the correct task ID prefix for new tasks

### 5. Clean Up After Merge
- Delete feature branches after successful merge
- Keep main branch clean and up to date

## Current Priority Tasks

### Immediate Next Steps
1. **STORY-001**: Add user profile page **PENDING**
2. **FIX-002**: Fix any remaining UI issues **PENDING**
3. **TECH-003**: Improve test coverage **PENDING**

### How to Start a New Task
```bash
# For a new feature
create_task_branch.bat STORY-001 feature user-profile-page

# For a bug fix
create_task_branch.bat FIX-002 fix ui-issue

# For a technical improvement
create_task_branch.bat TECH-003 tech improve-tests
```

## Troubleshooting

### Common Issues
1. **Branch already exists**: Delete the old branch first
2. **Not on main branch**: Switch to main before creating new branch
3. **Merge conflicts**: Resolve conflicts before continuing
4. **Wrong task ID prefix**: Use STORY-, FIX-, or TECH- based on task type

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
- Use the same format: `STORY-XXX: [Description]`, `FIX-XXX: [Description]`, `TECH-XXX: [Description]`
- Example: `STORY-001: Add user profile page`
- Example: `FIX-002: Fix database timeout issue`
- Example: `TECH-003: Add comprehensive test coverage`

### Pull Request Description
```
## Task ID
STORY-001

## Task Type
Feature/Enhancement

## Description
Add user profile page to the MBTI roster application.

## Changes Made
- Added profile page UI components
- Implemented profile data display
- Added profile editing functionality
- Added avatar upload feature

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing completed

## Related Issues
Closes #[issue-number]
```

This updated system ensures consistent task tracking, clear branch management, and professional development workflow with proper categorization of tasks by type. 