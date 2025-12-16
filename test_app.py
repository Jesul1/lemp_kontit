import sys
import requests

BASE_URL = "http://86.50.22.18/cicd/"

def check(endpoint):
    r = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
    assert r.status_code == 200, f"{endpoint} returned {r.status_code}"

try:
    check("/api/health")
    check("/api/wisdom")
except Exception as e:
    print("At least one API failed tests: ", str(e))
    sys.exit(1)

print("All tests passed!")