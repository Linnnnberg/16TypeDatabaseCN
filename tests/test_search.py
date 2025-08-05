"""
Search functionality regression tests
Tests hybrid search, suggestions, and analytics
"""
import requests
from tests.config import test_config

def test_basic_search():
    """Test basic search functionality"""
    try:
        response = test_config.make_request("GET", "/search/?q=周杰伦")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Basic Search",
            success,
            f"Status: {response.status_code}, Results: {data.get('total_results', 0)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Basic Search", False, str(e))
        return False

def test_search_by_name():
    """Test search by name only"""
    try:
        response = test_config.make_request("GET", "/search/?q=周杰伦&search_type=name")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search by Name",
            success,
            f"Status: {response.status_code}, Results: {data.get('total_results', 0)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search by Name", False, str(e))
        return False

def test_search_by_description():
    """Test search by description only"""
    try:
        response = test_config.make_request("GET", "/search/?q=歌手&search_type=description")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search by Description",
            success,
            f"Status: {response.status_code}, Results: {data.get('total_results', 0)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search by Description", False, str(e))
        return False

def test_search_by_tag():
    """Test search by tag only"""
    try:
        response = test_config.make_request("GET", "/search/?q=歌手&search_type=tag")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search by Tag",
            success,
            f"Status: {response.status_code}, Results: {data.get('total_results', 0)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search by Tag", False, str(e))
        return False

def test_search_by_mbti():
    """Test search by MBTI type"""
    try:
        response = test_config.make_request("GET", "/search/?q=INTJ&search_type=mbti")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search by MBTI",
            success,
            f"Status: {response.status_code}, Results: {data.get('total_results', 0)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search by MBTI", False, str(e))
        return False

def test_search_with_filters():
    """Test search with MBTI and tag filters"""
    try:
        response = test_config.make_request("GET", "/search/?q=周杰伦&mbti_type=INTJ&tag_filter=歌手")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search with Filters",
            success,
            f"Status: {response.status_code}, Results: {data.get('total_results', 0)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search with Filters", False, str(e))
        return False

def test_search_suggestions():
    """Test search suggestions/autocomplete"""
    try:
        response = test_config.make_request("GET", "/search/suggestions?q=周")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search Suggestions",
            success,
            f"Status: {response.status_code}, Suggestions: {len(data.get('suggestions', []))}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search Suggestions", False, str(e))
        return False

def test_search_analytics():
    """Test search analytics endpoint"""
    try:
        response = test_config.make_request("GET", "/search/analytics")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search Analytics",
            success,
            f"Status: {response.status_code}, Stats: {len(data.get('statistics', {}))}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search Analytics", False, str(e))
        return False

def test_mbti_types_endpoint():
    """Test MBTI types endpoint"""
    try:
        response = test_config.make_request("GET", "/search/mbti-types")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "MBTI Types Endpoint",
            success,
            f"Status: {response.status_code}, Types: {len(data.get('mbti_types', []))}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("MBTI Types Endpoint", False, str(e))
        return False

def test_popular_searches():
    """Test popular searches endpoint"""
    try:
        response = test_config.make_request("GET", "/search/popular-searches")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Popular Searches",
            success,
            f"Status: {response.status_code}, Searches: {len(data.get('popular_searches', []))}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Popular Searches", False, str(e))
        return False

def test_search_pagination():
    """Test search pagination"""
    try:
        response = test_config.make_request("GET", "/search/?q=周杰伦&skip=0&limit=5")
        success = response.status_code == 200
        data = response.json()
        pagination = data.get('pagination', {})
        test_config.add_test_result(
            "Search Pagination",
            success,
            f"Status: {response.status_code}, Limit: {pagination.get('limit', 0)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search Pagination", False, str(e))
        return False

def test_empty_search_query():
    """Test search with empty query (should fail)"""
    try:
        response = test_config.make_request("GET", "/search/?q=")
        success = response.status_code == 400  # Should fail
        test_config.add_test_result(
            "Empty Search Query",
            success,
            f"Status: {response.status_code}, Expected: 400"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Empty Search Query", False, str(e))
        return False

def run_search_tests():
    """Run all search functionality tests"""
    print("🔍 Running Search Functionality Tests...")
    
    tests = [
        test_basic_search,
        test_search_by_name,
        test_search_by_description,
        test_search_by_tag,
        test_search_by_mbti,
        test_search_with_filters,
        test_search_suggestions,
        test_search_analytics,
        test_mbti_types_endpoint,
        test_popular_searches,
        test_search_pagination,
        test_empty_search_query
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"✅ Search Functionality Tests: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    run_search_tests() 