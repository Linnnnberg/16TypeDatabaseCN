@echo off
REM Batch script to create new task branches
REM Usage: create_task_branch.bat 008 feature voting-endpoints

if "%3"=="" (
    echo Usage: create_task_branch.bat [TaskId] [Type] [Description]
    echo Example: create_task_branch.bat 008 feature voting-endpoints
    exit /b 1
)

set TaskId=%1
set Type=%2
set Description=%3

REM Format task ID with leading zeros
if %TaskId% LSS 100 (
    if %TaskId% LSS 10 (
        set FormattedTaskId=00%TaskId%
    ) else (
        set FormattedTaskId=0%TaskId%
    )
) else (
    set FormattedTaskId=%TaskId%
)

REM Create branch name
set BranchName=%Type%/TASK-%FormattedTaskId%-%Description%

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
    echo 1. Make your changes for TASK-%FormattedTaskId%
    echo 2. Commit your changes: git add . ^&^& git commit -m "TASK-%FormattedTaskId%: %Description%"
    echo 3. Push the branch: git push origin %BranchName%
    echo 4. Create a pull request on GitHub
) else (
    echo Error creating branch
    exit /b 1
) 