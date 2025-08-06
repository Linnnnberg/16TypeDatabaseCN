# Local CI/CD Pipeline Runner for Windows
# Runs all the same checks as GitHub Actions locally before pushing

param(
    [switch]$SkipInstall,
    [switch]$Quick
)

$ErrorActionPreference = "Continue"
$errors = @()
$warnings = @()
$successCount = 0
$totalChecks = 0

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host $Title -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
}

function Run-Command {
    param(
        [string]$Command,
        [string]$Description,
        [bool]$CheckOutput = $true,
        [bool]$CaptureOutput = $true
    )
    
    $script:totalChecks++
    Write-Header "Running: $Description"
    Write-Host "Command: $Command" -ForegroundColor Yellow
    
    try {
        if ($CaptureOutput) {
            $result = Invoke-Expression $Command 2>&1
            $exitCode = $LASTEXITCODE
            
            if ($result) {
                Write-Host "STDOUT:" -ForegroundColor Green
                Write-Host $result
            }
            
            if ($CheckOutput -and $exitCode -ne 0) {
                throw "Command failed with exit code $exitCode"
            }
            
            return $exitCode -eq 0
        } else {
            Invoke-Expression $Command
            $exitCode = $LASTEXITCODE
            
            if ($CheckOutput -and $exitCode -ne 0) {
                throw "Command failed with exit code $exitCode"
            }
            
            return $exitCode -eq 0
        }
    } catch {
        Write-Host "ERROR: $_" -ForegroundColor Red
        $script:errors += "$Description : $_"
        return $false
    }
}

function Install-Dependencies {
    Write-Header "INSTALLING DEPENDENCIES"
    
    if ($SkipInstall) {
        Write-Host "Skipping dependency installation (--SkipInstall flag)" -ForegroundColor Yellow
        return
    }
    
    # Install base requirements
    if (Run-Command "pip install -r requirements_minimal.txt" "Installing minimal requirements") {
        $script:successCount++
    }
    
    # Install testing dependencies
    if (Run-Command "pip install pytest pytest-cov pytest-asyncio" "Installing pytest dependencies") {
        $script:successCount++
    }
    
    # Install code quality tools
    if (Run-Command "pip install black flake8 mypy" "Installing code quality tools") {
        $script:successCount++
    }
    
    # Install security tools
    if (Run-Command "pip install bandit safety" "Installing security tools") {
        $script:successCount++
    }
    
    # Install additional tools
    if (Run-Command "pip install httpx pdoc3" "Installing additional tools") {
        $script:successCount++
    }
}

function Test-BlackFormatting {
    Write-Header "RUNNING BLACK CODE FORMATTING CHECK"
    
    # First, try to format the code
    if (Run-Command "python -m black app/ tests/" "Formatting code with Black" -CheckOutput:$false) {
        $script:successCount++
        Write-Host "✅ Black formatting completed" -ForegroundColor Green
    } else {
        $script:errors += "Black formatting failed"
        return $false
    }
    
    # Then check if formatting is correct
    if (Run-Command "python -m black --check app/ tests/" "Checking Black formatting") {
        $script:successCount++
        Write-Host "✅ Black formatting check passed" -ForegroundColor Green
        return $true
    } else {
        $script:errors += "Black formatting check failed"
        return $false
    }
}

function Test-Flake8Linting {
    Write-Header "RUNNING FLAKE8 LINTING CHECK"
    
    if (Run-Command "python -m flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503 --count --statistics" "Running Flake8 linting") {
        $script:successCount++
        Write-Host "✅ Flake8 linting passed" -ForegroundColor Green
        return $true
    } else {
        $script:errors += "Flake8 linting failed"
        return $false
    }
}

function Test-MyPyTypeChecking {
    Write-Header "RUNNING MYPY TYPE CHECKING"
    
    if (Run-Command "python -m mypy app/ --ignore-missing-imports" "Running MyPy type checking") {
        $script:successCount++
        Write-Host "✅ MyPy type checking passed" -ForegroundColor Green
        return $true
    } else {
        $script:errors += "MyPy type checking failed"
        return $false
    }
}

function Test-SecurityChecks {
    Write-Header "RUNNING SECURITY CHECKS"
    
    # Bandit security scan
    if (Run-Command "python -m bandit -r app/ -f json -o bandit-report.json" "Running Bandit security scan" -CheckOutput:$false) {
        $script:successCount++
        Write-Host "✅ Bandit security scan completed" -ForegroundColor Green
    } else {
        $script:warnings += "Bandit security scan failed or found issues"
    }
    
    # Safety dependency scan
    if (Run-Command "python -m safety check --json --output safety-report.json" "Running Safety dependency scan" -CheckOutput:$false) {
        $script:successCount++
        Write-Host "✅ Safety dependency scan completed" -ForegroundColor Green
    } else {
        $script:warnings += "Safety dependency scan failed or found issues"
    }
    
    return $true
}

function Test-Pytest {
    Write-Header "RUNNING TESTS WITH COVERAGE"
    
    if (Run-Command "python -m pytest tests/ --cov=app --cov-report=xml --cov-report=html --cov-report=term-missing -v" "Running tests with coverage" -CheckOutput:$false) {
        $script:successCount++
        Write-Host "✅ Tests completed" -ForegroundColor Green
        return $true
    } else {
        $script:errors += "Tests failed"
        return $false
    }
}

function Test-IntegrationTests {
    Write-Header "RUNNING INTEGRATION TESTS"
    
    if (Run-Command "python -m pytest tests/ -v --tb=short" "Running integration tests" -CheckOutput:$false) {
        $script:successCount++
        Write-Host "✅ Integration tests completed" -ForegroundColor Green
        return $true
    } else {
        $script:warnings += "Integration tests failed"
        return $false
    }
}

function Generate-Documentation {
    Write-Header "GENERATING DOCUMENTATION"
    
    # Create docs directory
    if (!(Test-Path "docs")) {
        New-Item -ItemType Directory -Path "docs" | Out-Null
    }
    
    if (Run-Command "python -m pdoc --html --output-dir docs/ app/" "Generating API documentation" -CheckOutput:$false) {
        $script:successCount++
        Write-Host "✅ Documentation generated" -ForegroundColor Green
        return $true
    } else {
        $script:warnings += "Documentation generation failed"
        return $false
    }
}

function Test-DockerBuild {
    Write-Header "CHECKING DOCKER BUILD"
    
    if (!(Test-Path "Dockerfile")) {
        Write-Host "⚠️  No Dockerfile found, skipping Docker build check" -ForegroundColor Yellow
        return $true
    }
    
    if (Run-Command "docker build -t mbti-roster:test ." "Building Docker image" -CheckOutput:$false) {
        $script:successCount++
        Write-Host "✅ Docker build successful" -ForegroundColor Green
        
        # Clean up
        Run-Command "docker rmi mbti-roster:test" "Cleaning up Docker image" -CheckOutput:$false
        return $true
    } else {
        $script:warnings += "Docker build failed"
        return $false
    }
}

function Show-Summary {
    Write-Header "LOCAL CI/CD SUMMARY"
    
    Write-Host "Total checks run: $totalChecks" -ForegroundColor White
    Write-Host "Successful checks: $successCount" -ForegroundColor Green
    Write-Host "Failed checks: $($errors.Count)" -ForegroundColor Red
    Write-Host "Warnings: $($warnings.Count)" -ForegroundColor Yellow
    
    if ($errors.Count -gt 0) {
        Write-Host ""
        Write-Host "❌ ERRORS ($($errors.Count)):" -ForegroundColor Red
        foreach ($error in $errors) {
            Write-Host "  - $error" -ForegroundColor Red
        }
    }
    
    if ($warnings.Count -gt 0) {
        Write-Host ""
        Write-Host "⚠️  WARNINGS ($($warnings.Count)):" -ForegroundColor Yellow
        foreach ($warning in $warnings) {
            Write-Host "  - $warning" -ForegroundColor Yellow
        }
    }
    
    if ($errors.Count -eq 0) {
        Write-Host ""
        Write-Host "✅ ALL CHECKS PASSED! Ready to push to GitHub." -ForegroundColor Green
        Write-Host "You can now run: git add . && git commit -m 'your message' && git push" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "❌ $($errors.Count) CHECKS FAILED. Please fix the issues before pushing." -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
}

# Main execution
Write-Host "🚀 Starting Local CI/CD Pipeline" -ForegroundColor Green
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

try {
    # Install dependencies
    Install-Dependencies
    
    # Run code quality checks
    Test-BlackFormatting
    Test-Flake8Linting
    Test-MyPyTypeChecking
    
    # Run security checks
    Test-SecurityChecks
    
    # Run tests
    Test-Pytest
    Test-IntegrationTests
    
    # Generate documentation
    Generate-Documentation
    
    # Check Docker build
    Test-DockerBuild
    
    # Show summary
    Show-Summary
    
    # Exit with appropriate code
    if ($errors.Count -eq 0) {
        exit 0
    } else {
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "❌ Unexpected error: $_" -ForegroundColor Red
    exit 1
} 