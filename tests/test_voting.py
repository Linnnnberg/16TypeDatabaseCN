"""
Voting system regression tests
Tests vote creation, retrieval, and MBTI type management
"""

from tests.config import test_config


def test_get_mbti_types():
    """Test getting all MBTI types"""
    try:
        response = test_config.make_request("GET", "/votes/mbti-types")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get MBTI Types",
            success,
            f"Status: {response.status_code}, Types: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get MBTI Types", False, str(e))
        return False


def test_get_all_votes():
    """Test getting all votes"""
    try:
        response = test_config.make_request("GET", "/votes/")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get All Votes",
            success,
            f"Status: {response.status_code}, Count: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get All Votes", False, str(e))
        return False


def test_create_vote():
    """Test creating a new vote"""
    try:
        # First get a celebrity to vote for
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                vote_data = {
                    "celebrity_id": celebrity_id,
                    "mbti_type": "INTJ",
                    "reason": "Test vote for regression testing",
                }
                response = test_config.make_request("POST", "/votes/", json=vote_data)
                success = response.status_code == 201
                test_config.add_test_result(
                    "Create Vote",
                    success,
                    f"Status: {response.status_code}, Celebrity: {celebrity_id}",
                )
                return success
            else:
                test_config.add_test_result(
                    "Create Vote", False, "No celebrities found"
                )
                return False
        else:
            test_config.add_test_result(
                "Create Vote", False, "Failed to get celebrities"
            )
            return False
    except Exception as e:
        test_config.add_test_result("Create Vote", False, str(e))
        return False


def test_get_user_votes():
    """Test getting votes for current user"""
    try:
        response = test_config.make_request("GET", "/votes/user")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get User Votes",
            success,
            f"Status: {response.status_code}, Count: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get User Votes", False, str(e))
        return False


def test_get_celebrity_votes():
    """Test getting votes for a specific celebrity"""
    try:
        # First get a celebrity
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                response = test_config.make_request(
                    "GET", f"/votes/celebrity/{celebrity_id}"
                )
                success = response.status_code == 200
                data = response.json()
                test_config.add_test_result(
                    "Get Celebrity Votes",
                    success,
                    f"Status: {response.status_code}, Count: {len(data)}",
                )
                return success
            else:
                test_config.add_test_result(
                    "Get Celebrity Votes", False, "No celebrities found"
                )
                return False
        else:
            test_config.add_test_result(
                "Get Celebrity Votes", False, "Failed to get celebrities"
            )
            return False
    except Exception as e:
        test_config.add_test_result("Get Celebrity Votes", False, str(e))
        return False


def test_get_vote_statistics():
    """Test getting vote statistics"""
    try:
        response = test_config.make_request("GET", "/votes/statistics")
        success = response.status_code == 200
        data = response.json()
        test_config.add_test_result(
            "Get Vote Statistics",
            success,
            f"Status: {response.status_code}, Stats: {len(data)}",
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get Vote Statistics", False, str(e))
        return False


def test_delete_vote():
    """Test deleting a vote"""
    try:
        # First get user votes to find one to delete
        response = test_config.make_request("GET", "/votes/user")
        if response.status_code == 200:
            votes = response.json()
            if votes:
                vote_id = votes[0]["id"]
                response = test_config.make_request("DELETE", f"/votes/{vote_id}")
                success = response.status_code == 204
                test_config.add_test_result(
                    "Delete Vote",
                    success,
                    f"Status: {response.status_code}, ID: {vote_id}",
                )
                return success
            else:
                test_config.add_test_result("Delete Vote", False, "No votes found")
                return False
        else:
            test_config.add_test_result(
                "Delete Vote", False, "Failed to get user votes"
            )
            return False
    except Exception as e:
        test_config.add_test_result("Delete Vote", False, str(e))
        return False


def test_duplicate_vote_validation():
    """Test that duplicate votes are prevented"""
    try:
        # First get a celebrity
        response = test_config.make_request("GET", "/celebrities/")
        if response.status_code == 200:
            celebrities = response.json()
            if celebrities:
                celebrity_id = celebrities[0]["id"]
                vote_data = {
                    "celebrity_id": celebrity_id,
                    "mbti_type": "INTP",
                    "reason": "Duplicate vote test",
                }
                # Create first vote
                response1 = test_config.make_request("POST", "/votes/", json=vote_data)
                if response1.status_code == 201:
                    # Try to create duplicate vote
                    response2 = test_config.make_request(
                        "POST", "/votes/", json=vote_data
                    )
                    success = response2.status_code == 400  # Should fail
                    test_config.add_test_result(
                        "Duplicate Vote Validation",
                        success,
                        f"First vote: {response1.status_code}, "
                        f"Second vote: {response2.status_code}",
                    )
                    return success
                else:
                    test_config.add_test_result(
                        "Duplicate Vote Validation",
                        False,
                        "Failed to create first vote",
                    )
                    return False
            else:
                test_config.add_test_result(
                    "Duplicate Vote Validation", False, "No celebrities found"
                )
                return False
        else:
            test_config.add_test_result(
                "Duplicate Vote Validation", False, "Failed to get celebrities"
            )
            return False
    except Exception as e:
        test_config.add_test_result("Duplicate Vote Validation", False, str(e))
        return False


def run_voting_tests():
    """Run all voting system tests"""
    print("Running Voting System Tests...")

    tests = [
        test_get_mbti_types,
        test_get_all_votes,
        test_create_vote,
        test_get_user_votes,
        test_get_celebrity_votes,
        test_get_vote_statistics,
        test_delete_vote,
        test_duplicate_vote_validation,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"Voting System Tests: {passed}/{total} passed")
    return passed == total


if __name__ == "__main__":
    run_voting_tests()
