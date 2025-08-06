@echo off
REM Batch script to create new task branches
REM Usage: create_task_branch.bat STORY-001 feature user-profile-page
REM Usage: create_task_branch.bat FIX-002 fix database-timeout
REM Usage: create_task_branch.bat TECH-003 tech add-test-coverage

if "%3"=="" (
    echo Usage: create_task_branch.bat [TaskId] [Type] [Description]
    echo.
    echo Task ID Format:
    echo   STORY-XXX for new features and enhancements
    echo   FIX-XXX for bug fixes and issue resolutions
    echo   TECH-XXX for technical improvements
    echo.
    echo Examples:
    echo   create_task_branch.bat STORY-001 feature user-profile-page
    echo   create_task_branch.bat FIX-002 fix database-timeout
    echo   create_task_branch.bat TECH-003 tech add-test-coverage
    exit /b 1
)

set TaskId=%1
set Type=%2
set Description=%3

REM Validate task ID format
echo %TaskId% | findstr /r "^STORY-[0-9][0-9][0-9]$" >nul
if %ERRORLEVEL% EQU 0 (
    set TaskPrefix=STORY
    goto :valid_task_id
)

echo %TaskId% | findstr /r "^FIX-[0-9][0-9][0-9]$" >nul
if %ERRORLEVEL% EQU 0 (
    set TaskPrefix=FIX
    goto :valid_task_id
)

echo %TaskId% | findstr /r "^TECH-[0-9][0-9][0-9]$" >nul
if %ERRORLEVEL% EQU 0 (
    set TaskPrefix=TECH
    goto :valid_task_id
)

echo Error: Invalid task ID format. Use STORY-XXX, FIX-XXX, or TECH-XXX
echo Example: STORY-001, FIX-002, TECH-003
exit /b 1

:valid_task_id

REM Create branch name based on task type
if "%Type%"=="feature" (
    set BranchName=feature/%TaskId%-%Description%
) else if "%Type%"=="fix" (
    set BranchName=fix/%TaskId%-%Description%
) else if "%Type%"=="tech" (
    set BranchName=tech/%TaskId%-%Description%
) else if "%Type%"=="hotfix" (
    set BranchName=hotfix/%TaskId%-%Description%
) else if "%Type%"=="docs" (
    set BranchName=docs/%TaskId%-%Description%
) else (
    echo Error: Invalid branch type. Use: feature, fix, tech, hotfix, or docs
    exit /b 1
)

echo Creating new branch: %BranchName%

REM Check if we're on main branch
for /f "tokens=*" %%i in ('git branch --show-current') do set CurrentBranch=%%i
if not "%CurrentBranch%"=="main" (
    echo Warning: You're not on the main branch. Current branch: %CurrentBranch%
    set /p Continue="Do you want to continue? (y/n): "
    if not "%Continue%"=="y" (
        echo Branch creation cancelled.
        exit /b 1
    )
)

REM Create and switch to new branch
git checkout -b %BranchName%
if %ERRORLEVEL% EQU 0 (
    echo Successfully created and switched to branch: %BranchName%
    echo.
    echo Current branch status:
    git status --short
    echo.
    echo Next steps:
    echo 1. Make your changes for %TaskId%
    echo 2. Commit your changes: git add . ^&^& git commit -m "%TaskId%: %Description%"
    echo 3. Push the branch: git push origin %BranchName%
    echo 4. Create a pull request on GitHub
    echo.
    echo Task Type: %TaskPrefix%
    echo Branch Type: %Type%
) else (
    echo Error creating branch
    exit /b 1
) 