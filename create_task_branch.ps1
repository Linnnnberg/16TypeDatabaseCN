# PowerShell script to create new task branches
# Usage: .\create_task_branch.ps1 -TaskId "STORY-001" -Type "feature" -Description "user-profile-page"
# Usage: .\create_task_branch.ps1 -TaskId "FIX-002" -Type "fix" -Description "database-timeout"
# Usage: .\create_task_branch.ps1 -TaskId "TECH-003" -Type "tech" -Description "add-test-coverage"

param(
    [Parameter(Mandatory=$true)]
    [string]$TaskId,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("feature", "fix", "tech", "hotfix", "docs")]
    [string]$Type,
    
    [Parameter(Mandatory=$true)]
    [string]$Description
)

# Validate task ID format
$TaskIdPattern = '^(STORY|FIX|TECH)-[0-9]{3}$'
if ($TaskId -notmatch $TaskIdPattern) {
    Write-Host "Error: Invalid task ID format. Use STORY-XXX, FIX-XXX, or TECH-XXX" -ForegroundColor Red
    Write-Host "Example: STORY-001, FIX-002, TECH-003" -ForegroundColor Yellow
    exit 1
}

# Extract task prefix
$TaskPrefix = $TaskId.Split('-')[0]

# Create branch name based on task type
switch ($Type) {
    "feature" { $BranchName = "feature/$TaskId-$Description" }
    "fix" { $BranchName = "fix/$TaskId-$Description" }
    "tech" { $BranchName = "tech/$TaskId-$Description" }
    "hotfix" { $BranchName = "hotfix/$TaskId-$Description" }
    "docs" { $BranchName = "docs/$TaskId-$Description" }
    default {
        Write-Host "Error: Invalid branch type. Use: feature, fix, tech, hotfix, or docs" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Creating new branch: $BranchName" -ForegroundColor Green

# Check if we're on main branch
$CurrentBranch = git branch --show-current
if ($CurrentBranch -ne "main") {
    Write-Host "Warning: You're not on the main branch. Current branch: $CurrentBranch" -ForegroundColor Yellow
    $Continue = Read-Host "Do you want to continue? (y/n)"
    if ($Continue -ne "y") {
        Write-Host "Branch creation cancelled." -ForegroundColor Red
        exit 1
    }
}

# Create and switch to new branch
try {
    git checkout -b $BranchName
    Write-Host "Successfully created and switched to branch: $BranchName" -ForegroundColor Green
    
    # Show current status
    Write-Host "`nCurrent branch status:" -ForegroundColor Cyan
    git status --short
    
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. Make your changes for $TaskId"
    Write-Host "2. Commit your changes: git add . && git commit -m '$TaskId`: $Description'"
    Write-Host "3. Push the branch: git push origin $BranchName"
    Write-Host "4. Create a pull request on GitHub"
    Write-Host ""
    Write-Host "Task Type: $TaskPrefix" -ForegroundColor Cyan
    Write-Host "Branch Type: $Type" -ForegroundColor Cyan
    
} catch {
    Write-Host "Error creating branch: $_" -ForegroundColor Red
    exit 1
} 