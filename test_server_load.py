#!/usr/bin/env python3
"""
Server Load Test
Check if server becomes unresponsive under load
"""

import requests
import time
import threading
import concurrent.futures

def make_request(request_id):
    """Make a single request"""
    try:
        start_time = time.time()
        response = requests.post("http://localhost:8000/auth/signup", 
                               json={
                                   "name": f"Load Test User {request_id}",
                                   "email": f"loadtest{request_id}_{int(time.time())}@example.com",
                                   "password": "testpass123"
                               },
                               timeout=10)
        end_time = time.time()
        
        if response.status_code == 201:
            print(f"Request {request_id}: SUCCESS ({end_time - start_time:.2f}s)")
            return True
        else:
            print(f"Request {request_id}: FAILED {response.status_code} ({end_time - start_time:.2f}s)")
            return False
    except requests.exceptions.Timeout:
        print(f"Request {request_id}: TIMEOUT")
        return False
    except Exception as e:
        print(f"Request {request_id}: ERROR {e}")
        return False

def test_server_load():
    print("Server Load Test")
    print("=" * 50)
    
    # Test 1: Single request baseline
    print("\n1. Single Request Baseline...")
    success = make_request(0)
    if not success:
        print("Baseline request failed - server may be down")
        return
    
    # Test 2: Multiple concurrent requests
    print("\n2. Multiple Concurrent Requests...")
    num_requests = 5
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(make_request, i) for i in range(1, num_requests + 1)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    success_count = sum(results)
    print(f"\nResults: {success_count}/{num_requests} requests succeeded")
    
    if success_count < num_requests:
        print("Server is having issues under load!")
    else:
        print("Server handles load well")

if __name__ == "__main__":
    test_server_load()
