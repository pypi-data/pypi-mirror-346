# tests/test_registry_smoke.py

import httpx
import pytest

BASE_URL = "http://localhost:8000"

@pytest.mark.skipif("CI" in __import__("os").environ, reason="CI does not run the service")
def test_docs_available():
    """Ensure FastAPI docs route is up (if running locally)."""
    try:
        r = httpx.get(f"{BASE_URL}/docs")
        assert r.status_code == 200
    except httpx.ConnectError:
        pytest.skip("Registry service not running locally.")
