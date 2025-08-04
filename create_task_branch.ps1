# PowerShell script to create new task branches
# Usage: .\create_task_branch.ps1 -TaskId "008" -Type "feature" -Description "voting-endpoints"

param(
    [Parameter(Mandatory=$true)]
    [string]$TaskId,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("feature", "fix", "hotfix", "docs")]
    [string]$Type,
    
    [Parameter(Mandatory=$true)]
    [string]$Description
)

# Format task ID with leading zeros
$FormattedTaskId = $TaskId.PadLeft(3, '0')

# Create branch name
$BranchName = "$Type/TASK-$FormattedTaskId-$Description"

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
    Write-Host "1. Make your changes for TASK-$FormattedTaskId"
    Write-Host "2. Commit your changes: git add . && git commit -m 'TASK-$FormattedTaskId`: $Description'"
    Write-Host "3. Push the branch: git push origin $BranchName"
    Write-Host "4. Create a pull request on GitHub"
    
} catch {
    Write-Host "Error creating branch: $_" -ForegroundColor Red
    exit 1
} 