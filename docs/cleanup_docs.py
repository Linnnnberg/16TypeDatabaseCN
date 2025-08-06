#!/usr/bin/env python3
"""
Documentation Cleanup and Validation Script
Helps maintain clean and organized documentation
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple


class DocumentationManager:
    """Manages documentation cleanup and validation"""
    
    def __init__(self):
        self.root_dir = Path(".")
        self.docs_dir = Path("docs")
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def add_error(self, message: str):
        """Add an error message"""
        self.errors.append(message)
        
    def add_warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(message)
        
    def add_success(self, message: str):
        """Add a success message"""
        self.success_count += 1
        print(f"SUCCESS: {message}")
        
    def check_documentation_structure(self) -> bool:
        """Check documentation file organization"""
        print("\n" + "="*60)
        print("CHECKING DOCUMENTATION STRUCTURE")
        print("="*60)
        
        # Expected documentation files
        expected_files = [
            "README.md",
            "DEVELOPMENT_GUIDELINES.md",
            "CI_CD_RULES.md",
            "CI_CD_GUIDE.md",
            "LOCAL_DEVELOPMENT.md",
            "API_DOCUMENTATION.md",
            "TODO.md",
            "TECH_TASKS.md",
            "TASK_ID_GUIDE.md",
            "DEVELOPMENT_CYCLE_ANALYSIS.md",
            "RECENT_IMPROVEMENTS.md",
            "MVP_Frontend_Plan.md"
        ]
        
        missing_files = []
        for file_name in expected_files:
            if not (self.root_dir / file_name).exists():
                missing_files.append(file_name)
        
        if missing_files:
            print("WARNING: Missing expected documentation files:")
            for file_name in missing_files:
                print(f"  - {file_name}")
            self.add_warning(f"Missing {len(missing_files)} expected documentation files")
        else:
            self.add_success("All expected documentation files exist")
            
        # Check docs directory structure
        if not self.docs_dir.exists():
            self.add_error("docs/ directory not found")
            return False
            
        if not (self.docs_dir / "README.md").exists():
            self.add_error("docs/README.md not found")
            return False
            
        self.add_success("Documentation structure is properly organized")
        return True
        
    def check_markdown_links(self) -> bool:
        """Check for broken markdown links"""
        print("\n" + "="*60)
        print("CHECKING MARKDOWN LINKS")
        print("="*60)
        
        markdown_files = list(self.root_dir.rglob("*.md"))
        broken_links = []
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find markdown links
                link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                matches = re.findall(link_pattern, content)
                
                for link_text, link_url in matches:
                    # Skip external links
                    if link_url.startswith(('http://', 'https://', 'mailto:')):
                        continue
                        
                    # Handle relative links
                    if link_url.startswith('../'):
                        target_path = file_path.parent.parent / link_url[3:]
                    elif link_url.startswith('./'):
                        target_path = file_path.parent / link_url[2:]
                    elif link_url.startswith('/'):
                        target_path = self.root_dir / link_url[1:]
                    else:
                        target_path = file_path.parent / link_url
                    
                    # Check if target exists
                    if not target_path.exists():
                        broken_links.append(f"{file_path}: {link_text} -> {link_url}")
                        
            except Exception as e:
                self.add_warning(f"Could not check {file_path}: {e}")
        
        if broken_links:
            print("ERROR: Found broken markdown links:")
            for link in broken_links:
                print(f"  - {link}")
            self.add_error(f"Found {len(broken_links)} broken links")
            return False
        else:
            self.add_success("All markdown links are valid")
            return True
            
    def check_documentation_consistency(self) -> bool:
        """Check documentation consistency and formatting"""
        print("\n" + "="*60)
        print("CHECKING DOCUMENTATION CONSISTENCY")
        print("="*60)
        
        markdown_files = list(self.root_dir.rglob("*.md"))
        issues = []
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # Check for consistent heading structure
                heading_levels = []
                for i, line in enumerate(lines, 1):
                    if line.startswith('#'):
                        level = len(line) - len(line.lstrip('#'))
                        heading_levels.append((level, i, line.strip()))
                
                # Check for skipped heading levels
                for i in range(len(heading_levels) - 1):
                    current_level = heading_levels[i][0]
                    next_level = heading_levels[i + 1][0]
                    if next_level > current_level + 1:
                        issues.append(f"{file_path}:{heading_levels[i+1][1]}: Skipped heading level")
                
                # Check for proper file structure
                if not content.strip():
                    issues.append(f"{file_path}: Empty file")
                    
                if not content.startswith('# '):
                    issues.append(f"{file_path}: Missing main heading")
                    
                # Check for consistent line endings
                if '\r\n' in content:
                    issues.append(f"{file_path}: Mixed line endings detected")
                    
            except Exception as e:
                self.add_warning(f"Could not check {file_path}: {e}")
        
        if issues:
            print("WARNING: Found documentation consistency issues:")
            for issue in issues:
                print(f"  - {issue}")
            self.add_warning(f"Found {len(issues)} consistency issues")
        else:
            self.add_success("Documentation formatting is consistent")
            
        return True
        
    def check_outdated_documentation(self) -> bool:
        """Check for potentially outdated documentation"""
        print("\n" + "="*60)
        print("CHECKING FOR OUTDATED DOCUMENTATION")
        print("="*60)
        
        # Check for TODO comments in documentation
        markdown_files = list(self.root_dir.rglob("*.md"))
        todo_items = []
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find TODO, FIXME, NOTE comments
                todo_pattern = r'(TODO|FIXME|NOTE|XXX):\s*(.+)'
                matches = re.findall(todo_pattern, content, re.IGNORECASE)
                
                for todo_type, message in matches:
                    todo_items.append(f"{file_path}: {todo_type}: {message.strip()}")
                    
            except Exception as e:
                self.add_warning(f"Could not check {file_path}: {e}")
        
        if todo_items:
            print("INFO: Found documentation items that need attention:")
            for item in todo_items[:10]:  # Show first 10
                print(f"  - {item}")
            if len(todo_items) > 10:
                print(f"  ... and {len(todo_items) - 10} more")
            self.add_warning(f"Found {len(todo_items)} items needing attention")
        else:
            self.add_success("No obvious outdated documentation found")
            
        return True
        
    def generate_documentation_report(self) -> bool:
        """Generate a documentation status report"""
        print("\n" + "="*60)
        print("GENERATING DOCUMENTATION REPORT")
        print("="*60)
        
        markdown_files = list(self.root_dir.rglob("*.md"))
        total_files = len(markdown_files)
        total_lines = 0
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
            except Exception:
                pass
        
        print(f"Documentation Statistics:")
        print(f"  - Total markdown files: {total_files}")
        print(f"  - Total lines of documentation: {total_lines:,}")
        print(f"  - Average lines per file: {total_lines // total_files if total_files > 0 else 0}")
        
        # File size analysis
        large_files = []
        for file_path in markdown_files:
            try:
                size = file_path.stat().st_size
                if size > 50 * 1024:  # 50KB
                    large_files.append(f"{file_path}: {size // 1024}KB")
            except Exception:
                pass
        
        if large_files:
            print(f"  - Large files (>50KB): {len(large_files)}")
            for file_info in large_files:
                print(f"    - {file_info}")
        
        self.add_success("Documentation report generated")
        return True
        
    def suggest_improvements(self) -> bool:
        """Suggest documentation improvements"""
        print("\n" + "="*60)
        print("SUGGESTING DOCUMENTATION IMPROVEMENTS")
        print("="*60)
        
        suggestions = []
        
        # Check for missing documentation
        if not (self.root_dir / "CHANGELOG.md").exists():
            suggestions.append("Create CHANGELOG.md to track version changes")
            
        if not (self.root_dir / "CONTRIBUTING.md").exists():
            suggestions.append("Create CONTRIBUTING.md for contribution guidelines")
            
        if not (self.docs_dir / "API.md").exists():
            suggestions.append("Create docs/API.md for detailed API documentation")
            
        # Check for documentation coverage
        code_dirs = ["app", "tests"]
        for code_dir in code_dirs:
            if Path(code_dir).exists():
                py_files = list(Path(code_dir).rglob("*.py"))
                if py_files and not any(f"{code_dir}_README.md" in str(f) for f in self.root_dir.glob("*.md")):
                    suggestions.append(f"Create {code_dir.upper()}_README.md for {code_dir} documentation")
        
        if suggestions:
            print("SUGGESTIONS for documentation improvement:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        else:
            print("Documentation appears to be well-covered")
            
        self.add_success("Documentation improvement suggestions generated")
        return True
        
    def run_all_checks(self) -> bool:
        """Run all documentation checks"""
        print("STARTING: Documentation Cleanup and Validation")
        print("="*60)
        
        checks = [
            ("Documentation Structure", self.check_documentation_structure),
            ("Markdown Links", self.check_markdown_links),
            ("Documentation Consistency", self.check_documentation_consistency),
            ("Outdated Documentation", self.check_outdated_documentation),
            ("Generate Report", self.generate_documentation_report),
            ("Suggest Improvements", self.suggest_improvements),
        ]
        
        passed_checks = 0
        total_checks = len(checks)
        
        for check_name, check_func in checks:
            print(f"\nRunning: {check_name}")
            try:
                if check_func():
                    passed_checks += 1
            except Exception as e:
                self.add_error(f"{check_name} check failed with exception: {e}")
        
        # Print summary
        print("\n" + "="*60)
        print("DOCUMENTATION CLEANUP SUMMARY")
        print("="*60)
        
        print(f"Total checks: {total_checks}")
        print(f"Passed checks: {passed_checks}")
        print(f"Failed checks: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\nERROR: ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\nWARNING: WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors:
            print(f"\nSUCCESS: Documentation is well-organized and maintained!")
        else:
            print(f"\nERROR: {len(self.errors)} documentation issues found.")
            print("Please address the issues to improve documentation quality.")
        
        return len(self.errors) == 0


def main():
    """Main function"""
    manager = DocumentationManager()
    
    try:
        success = manager.run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nERROR: Documentation cleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
