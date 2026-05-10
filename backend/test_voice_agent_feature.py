"""
Test: Voice Agent Feature (3rd button on home page)
Run: python test_voice_agent_feature.py
Make sure backend is running on http://127.0.0.1:8000
"""

import httpx

BASE = "http://127.0.0.1:8000/api"


def test_voice_agent_health():
    print("\n--- Test 1: Voice Agent Health ---")
    res = httpx.get(f"{BASE}/voice-agent-health", timeout=10)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.json()}")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print("✅ PASSED")


def test_text_agent_send_button():
    print("\n--- Test 2: Send Button (type your question) ---")
    res = httpx.post(
        f"{BASE}/text-agent",
        json={"text": "What is 2 + 2?", "voiceId": "21m00Tcm4TlvDq8ikWAM"},
        timeout=60,
    )
    print(f"Status: {res.status_code}")

    if res.status_code == 200:
        data = res.json()
        print(f"You said : {data.get('userText')}")
        print(f"AI replied: {data.get('text')}")
        print(f"Audio     : {'✅ received' if data.get('audio') else '❌ missing'}")
        assert data.get("userText")
        assert data.get("text")
        print("✅ PASSED")
    else:
        print(f"❌ FAILED — {res.text}")


def test_text_agent_empty_input():
    print("\n--- Test 3: Empty input should be rejected ---")
    res = httpx.post(
        f"{BASE}/text-agent",
        json={"text": "   ", "voiceId": "21m00Tcm4TlvDq8ikWAM"},
        timeout=10,
    )
    print(f"Status: {res.status_code}")
    assert res.status_code == 400
    print("✅ PASSED — backend correctly rejected empty input")


if __name__ == "__main__":
    print("=" * 50)
    print("  Voice Agent Feature Tests (3rd button)")
    print("=" * 50)

    try:
        test_voice_agent_health()
        test_text_agent_send_button()
        test_text_agent_empty_input()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except httpx.ConnectError:
        print("\n❌ Cannot connect — make sure backend is running: uvicorn main:app --reload")
