"""
Celebrity management system regression tests
Tests CRUD operations, search, and tag management
"""

import requests
from tests.config import test_config


def test_get_all_celebrities():
    """Test getting all celebrities"""
    try:
        response = test_config.make_request("GET", "/celebrities/")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get All Celebrities",
            success,
            f"Status: {response.status_code}, Count: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get All Celebrities", False, str(e))
        return False


def test_get_celebrity_by_id():
    """Test getting a specific celebrity by ID"""
    try:
        # First get all celebrities to get an ID
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                response = test_config.make_request(
                    "GET", f"/celebrities/{celebrity_id}"
                )
                success = response.status_code == 200
                test_config.add_test_result(
                    "Get Celebrity by ID",
                    success,
                    f"Status: {response.status_code}, ID: {celebrity_id}",
                )
                return success
            else:
                test_config.add_test_result(
                    "Get Celebrity by ID", False, "No celebrities found"
                )
                return False
        else:
            test_config.add_test_result(
                "Get Celebrity by ID", False, "Failed to get celebrities list"
            )
            return False
    except Exception as e:
        test_config.add_test_result("Get Celebrity by ID", False, str(e))
        return False


def test_search_celebrities():
    """Test celebrity search functionality"""
    try:
        response = test_config.make_request("GET", "/celebrities/?search=周杰伦")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Search Celebrities",
            success,
            f"Status: {response.status_code}, Results: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Search Celebrities", False, str(e))
        return False


def test_get_popular_celebrities():
    """Test getting popular celebrities"""
    try:
        response = test_config.make_request("GET", "/celebrities/popular")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get Popular Celebrities",
            success,
            f"Status: {response.status_code}, Count: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get Popular Celebrities", False, str(e))
        return False


def test_get_celebrities_by_tag():
    """Test getting celebrities by tag"""
    try:
        response = test_config.make_request("GET", "/celebrities/tag/歌手")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get Celebrities by Tag",
            success,
            f"Status: {response.status_code}, Count: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get Celebrities by Tag", False, str(e))
        return False


def test_create_celebrity():
    """Test creating a new celebrity (admin only)"""
    try:
        new_celebrity = {
            "name": "Test Celebrity",
            "name_en": "Test Celebrity EN",
            "description": "A test celebrity for regression testing",
            "image_url": "https://example.com/test.jpg",
        }
        response = test_config.make_request("POST", "/celebrities/", json=new_celebrity)
        success = response.status_code == 201
        test_config.add_test_result(
            "Create Celebrity",
            success,
            f"Status: {response.status_code}, Response: {response.text}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Create Celebrity", False, str(e))
        return False


def test_update_celebrity():
    """Test updating a celebrity (admin only)"""
    try:
        # First get a celebrity to update
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                update_data = {"description": "Updated description for testing"}
                response = test_config.make_request(
                    "PUT", f"/celebrities/{celebrity_id}", json=update_data
                )
                success = response.status_code == 200
                test_config.add_test_result(
                    "Update Celebrity",
                    success,
                    f"Status: {response.status_code}, ID: {celebrity_id}",
                )
                return success
            else:
                test_config.add_test_result(
                    "Update Celebrity", False, "No celebrities found"
                )
                return False
        else:
            test_config.add_test_result(
                "Update Celebrity", False, "Failed to get celebrities"
            )
            return False
    except Exception as e:
        test_config.add_test_result("Update Celebrity", False, str(e))
        return False


def test_add_tag_to_celebrity():
    """Test adding a tag to a celebrity (admin only)"""
    try:
        # First get a celebrity
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                response = test_config.make_request(
                    "POST", f"/celebrities/{celebrity_id}/tags/test-tag"
                )
                success = response.status_code == 201
                test_config.add_test_result(
                    "Add Tag to Celebrity",
                    success,
                    f"Status: {response.status_code}, ID: {celebrity_id}",
                )
                return success
            else:
                test_config.add_test_result(
                    "Add Tag to Celebrity", False, "No celebrities found"
                )
                return False
        else:
            test_config.add_test_result(
                "Add Tag to Celebrity", False, "Failed to get celebrities"
            )
            return False
    except Exception as e:
        test_config.add_test_result("Add Tag to Celebrity", False, str(e))
        return False


def run_celebrities_tests():
    """Run all celebrity management tests"""
    print("Running Celebrity Management Tests...")

    tests = [
        test_get_all_celebrities,
        test_get_celebrity_by_id,
        test_search_celebrities,
        test_get_popular_celebrities,
        test_get_celebrities_by_tag,
        test_create_celebrity,
        test_update_celebrity,
        test_add_tag_to_celebrity,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"Celebrity Management Tests: {passed}/{total} passed")
    return passed == total


if __name__ == "__main__":
    run_celebrities_tests()
