"""
Comment system regression tests
Tests comment creation, retrieval, and nested replies
"""
import requests
from tests.config import test_config

def test_get_all_comments():
    """Test getting all comments"""
    try:
        response = test_config.make_request("GET", "/comments/")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get All Comments",
            success,
            f"Status: {response.status_code}, Count: {len(data)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get All Comments", False, str(e))
        return False

def test_create_comment():
    """Test creating a new comment"""
    try:
        # First get a celebrity to comment on
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                comment_data = {
                    "celebrity_id": celebrity_id,
                    "content": "Test comment for regression testing"
                }
                response = test_config.make_request("POST", "/comments/", json=comment_data)
                success = response.status_code == 201
                test_config.add_test_result(
                    "Create Comment",
                    success,
                    f"Status: {response.status_code}, Celebrity: {celebrity_id}"
                )
                return success
            else:
                test_config.add_test_result("Create Comment", False, "No celebrities found")
                return False
        else:
            test_config.add_test_result("Create Comment", False, "Failed to get celebrities")
            return False
    except Exception as e:
        test_config.add_test_result("Create Comment", False, str(e))
        return False

def test_get_user_comments():
    """Test getting comments for current user"""
    try:
        response = test_config.make_request("GET", "/comments/user")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get User Comments",
            success,
            f"Status: {response.status_code}, Count: {len(data)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get User Comments", False, str(e))
        return False

def test_get_celebrity_comments():
    """Test getting comments for a specific celebrity"""
    try:
        # First get a celebrity
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                response = test_config.make_request("GET", f"/comments/celebrity/{celebrity_id}")
                success = response.status_code == 200
                data = response.json()
                test_config.add_test_result(
                    "Get Celebrity Comments",
                    success,
                    f"Status: {response.status_code}, Count: {len(data)}"
                )
                return success
            else:
                test_config.add_test_result("Get Celebrity Comments", False, "No celebrities found")
                return False
        else:
            test_config.add_test_result("Get Celebrity Comments", False, "Failed to get celebrities")
            return False
    except Exception as e:
        test_config.add_test_result("Get Celebrity Comments", False, str(e))
        return False

def test_create_reply():
    """Test creating a reply to a comment"""
    try:
        # First get user comments to find one to reply to
        response = test_config.make_request("GET", "/comments/user")
        if response.status_code == 200:
            comments = response.json()
            if comments:
                parent_id = comments[0]["id"]
                reply_data = {
                    "celebrity_id": comments[0]["celebrity_id"],
                    "content": "Test reply for regression testing",
                    "parent_id": parent_id
                }
                response = test_config.make_request("POST", "/comments/", json=reply_data)
                success = response.status_code == 201
                test_config.add_test_result(
                    "Create Reply",
                    success,
                    f"Status: {response.status_code}, Parent: {parent_id}"
                )
                return success
            else:
                test_config.add_test_result("Create Reply", False, "No comments found")
                return False
        else:
            test_config.add_test_result("Create Reply", False, "Failed to get user comments")
            return False
    except Exception as e:
        test_config.add_test_result("Create Reply", False, str(e))
        return False

def test_update_comment():
    """Test updating a comment"""
    try:
        # First get user comments to find one to update
        response = test_config.make_request("GET", "/comments/user")
        if response.status_code == 200:
            comments = response.json()
            if comments:
                comment_id = comments[0]["id"]
                update_data = {
                    "content": "Updated comment content for testing"
                }
                response = test_config.make_request("PUT", f"/comments/{comment_id}", json=update_data)
                success = response.status_code == 200
                test_config.add_test_result(
                    "Update Comment",
                    success,
                    f"Status: {response.status_code}, ID: {comment_id}"
                )
                return success
            else:
                test_config.add_test_result("Update Comment", False, "No comments found")
                return False
        else:
            test_config.add_test_result("Update Comment", False, "Failed to get user comments")
            return False
    except Exception as e:
        test_config.add_test_result("Update Comment", False, str(e))
        return False

def test_delete_comment():
    """Test deleting a comment"""
    try:
        # First get user comments to find one to delete
        response = test_config.make_request("GET", "/comments/user")
        if response.status_code == 200:
            comments = response.json()
            if comments:
                comment_id = comments[0]["id"]
                response = test_config.make_request("DELETE", f"/comments/{comment_id}")
                success = response.status_code == 204
                test_config.add_test_result(
                    "Delete Comment",
                    success,
                    f"Status: {response.status_code}, ID: {comment_id}"
                )
                return success
            else:
                test_config.add_test_result("Delete Comment", False, "No comments found")
                return False
        else:
            test_config.add_test_result("Delete Comment", False, "Failed to get user comments")
            return False
    except Exception as e:
        test_config.add_test_result("Delete Comment", False, str(e))
        return False

def test_get_comment_statistics():
    """Test getting comment statistics"""
    try:
        response = test_config.make_request("GET", "/comments/statistics")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get Comment Statistics",
            success,
            f"Status: {response.status_code}, Stats: {len(data)}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get Comment Statistics", False, str(e))
        return False

def run_comments_tests():
    """Run all comment system tests"""
    print("💬 Running Comment System Tests...")
    
    tests = [
        test_get_all_comments,
        test_create_comment,
        test_get_user_comments,
        test_get_celebrity_comments,
        test_create_reply,
        test_update_comment,
        test_delete_comment,
        test_get_comment_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"✅ Comment System Tests: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    run_comments_tests() 