#!/usr/bin/env python3
"""
Simple test runner for MBTI Roster regression tests
Usage: python run_tests.py [test_suite]
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Main function to run tests"""
    if len(sys.argv) > 1:
        test_suite = sys.argv[1].lower()
        
        if test_suite == "auth":
            from tests.test_auth import run_auth_tests
            run_auth_tests()
        elif test_suite == "celebrities":
            from tests.test_celebrities import run_celebrities_tests
            run_celebrities_tests()
        elif test_suite == "voting":
            from tests.test_voting import run_voting_tests
            run_voting_tests()
        elif test_suite == "comments":
            from tests.test_comments import run_comments_tests
            run_comments_tests()
        elif test_suite == "search":
            from tests.test_search import run_search_tests
            run_search_tests()
        else:
            print(f"Unknown test suite: {test_suite}")
            print("Available test suites: auth, celebrities, voting, comments, search")
            sys.exit(1)
    else:
        # Run all tests
        from tests.run_all_tests import main as run_all_tests
        run_all_tests()

if __name__ == "__main__":
    main() 