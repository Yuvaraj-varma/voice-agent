import requests
import sys

BACKEND = "http://127.0.0.1:8000/api"

def test_endpoint(name, url, method="GET"):
    try:
        if method == "GET":
            r = requests.get(url, timeout=5)
        else:
            r = requests.post(url, timeout=5)
        
        status = "OK" if r.status_code < 500 else "FAIL"
        print(f"{status} {name}: {r.status_code}")
        return r.status_code < 500
    except Exception as e:
        print(f"FAIL {name}: {e}")
        return False

print("Testing Backend Endpoints...\n")

results = []
results.append(test_endpoint("Health Check", "http://127.0.0.1:8000/health"))
results.append(test_endpoint("Get Voices", f"{BACKEND}/voices"))
results.append(test_endpoint("Voice Agent Health", f"{BACKEND}/voice-agent-health"))

print(f"\n{sum(results)}/{len(results)} endpoints working")
sys.exit(0 if all(results) else 1)
