"""
Expanded pytest suite to probe edge-cases and potential implementation holes
in the registry-service API.
"""
import pytest
import httpx
import uuid
import time
import re
from datetime import datetime

BASE_URL = "http://testserver"  # Unused when using TestClient

@pytest.fixture(scope="session")
def client(tmp_path_factory):
    # Override the SQLite DB path for isolation
    import registry_service.service as service
    db_file = tmp_path_factory.mktemp("data") / "test_registry.sqlite"
    service.db_path = str(db_file)
    # Use FastAPI TestClient for in-process testing
    from fastapi.testclient import TestClient
    from registry_service.service import app
    with TestClient(app) as client:
        yield client

@pytest.fixture
def rand_name():
    return f"test_{uuid.uuid4().hex}"

def parse_iso_datetime(dt_str: str) -> datetime:
    # Normalize trailing Z to +00:00 for fromisoformat
    if dt_str.endswith("Z"):
        dt_str = dt_str[:-1] + "+00:00"
    return datetime.fromisoformat(dt_str)

def test_registered_at_has_timezone(client, rand_name):
    data = {"category": "semantic_label", "name": rand_name, "description": "timestamp test"}
    r = client.post("/register", json=data)
    assert r.status_code == 200
    res = r.json()
    ts = res.get("registered_at")
    assert ts and re.match(r".*(Z|\+00:00)$", ts)
    dt = parse_iso_datetime(ts)
    assert dt.tzinfo is not None

def test_same_name_different_categories_allowed(client, rand_name):
    name = rand_name
    cats = ("llm", "analyzer")
    uids = []
    for cat in cats:
        r = client.post("/register", json={"category": cat, "name": name, "description": "dup allowed"})
        assert r.status_code == 200, f"Failed for category {cat}: {r.text}"
        uids.append(r.json()["uuid"])
    # Should be two distinct UUIDs
    assert len(set(uids)) == 2

def test_register_immutable_mapping(client, rand_name):
    name = rand_name
    category = "semantic_label"
    # First registration should succeed
    r1 = client.post("/register", json={
        "category": category,
        "name": name,
        "description": "initial description"
    })
    assert r1.status_code == 200

    # Second registration with same name/category but different description or cookie must conflict
    r2 = client.post("/register", json={
        "category": category,
        "name": name,
        "description": "modified description",
        "cookie": {"note": "attempt to modify mapping"}
    })
    assert r2.status_code == 409

def test_register_cookie_roundtrip(client, rand_name):
    # POST /register with a cookie, then GET /resolve to verify cookie is returned
    name = rand_name
    category = "semantic_label"
    cookie = {"note": "initial cookie", "count": 5}
    # Register with cookie
    r1 = client.post("/register", json={
        "category": category,
        "name": name,
        "description": "cookie roundtrip test",
        "cookie": cookie
    })
    assert r1.status_code == 200
    res1 = r1.json()
    uid = res1.get("uuid")
    # Resolve and check cookie
    r2 = client.get("/resolve", params={"category": category, "name": name})
    assert r2.status_code == 200
    res2 = r2.json()
    assert res2.get("uuid") == uid
    assert res2.get("cookie") == cookie

def test_register_invalid_schema_type(client, rand_name):
    # schema must be an object or null
    payload = {"category": "llm", "name": rand_name, "description": "x", "schema": "not a dict"}
    r = client.post("/register", json=payload)
    assert r.status_code == 422

def test_register_invalid_cookie_list(client, rand_name):
    # cookie must be an object or null
    payload = {"category": "llm", "name": rand_name, "description": "x", "cookie": ["not", "a", "dict"]}
    r = client.post("/register", json=payload)
    assert r.status_code == 422

def test_register_invalid_cookie_string(client, rand_name):
    # cookie must be an object or null
    payload = {"category": "llm", "name": rand_name, "description": "x", "cookie": "string"}
    r = client.post("/register", json=payload)
    assert r.status_code == 422

def test_missing_required_fields(client):
    # Missing name
    r = client.post("/register", json={"category": "llm", "description": "x"})
    assert r.status_code == 422
    # Missing category
    r = client.post("/register", json={"name": "x", "description": "y"})
    assert r.status_code == 422
    # Missing description
    r = client.post("/register", json={"category": "llm", "name": "x"})
    assert r.status_code == 422

def test_invalid_category(client, rand_name):
    r = client.post("/register", json={"category": "nope", "name": rand_name, "description": "x"})
    assert r.status_code == 422

def test_resolve_unknown_and_mismatch(client, rand_name):
    # Unknown name
    r = client.get("/resolve", params={"category": "llm", "name": rand_name})
    assert r.status_code == 404
    # Register then mismatch
    r1 = client.post("/register", json={"category": "llm", "name": rand_name, "description": "x"})
    assert r1.status_code == 200
    r2 = client.get("/resolve", params={"category": "analyzer", "name": rand_name})
    assert r2.status_code == 404

def test_set_properties_invalid_uuid(client):
    bad_uuid = str(uuid.uuid4())
    payload = {"uuid": bad_uuid, "category": "analyzer", "properties": {"a": 1}}
    r = client.post("/properties", json=payload)
    assert r.status_code == 404

def test_set_properties_category_mismatch(client, rand_name):
    # Register under one category
    r1 = client.post("/register", json={"category": "llm", "name": rand_name, "description": "x"})
    assert r1.status_code == 200
    uid = r1.json()["uuid"]
    # Attempt with wrong category
    payload = {"uuid": uid, "category": "analyzer", "properties": {}}
    r2 = client.post("/properties", json=payload)
    # Category mismatch is treated as not found
    assert r2.status_code == 404

def test_properties_missing_properties_field(client, rand_name):
    r = client.post("/register", json={"category": "analyzer", "name": rand_name, "description": "x"})
    assert r.status_code == 200
    uid = r.json()["uuid"]
    payload = {"uuid": uid, "category": "analyzer"}
    r2 = client.post("/properties", json=payload)
    assert r2.status_code == 422

def test_nested_properties_and_null_cookie(client, rand_name):
    r = client.post("/register", json={"category": "analyzer", "name": rand_name, "description": "x"})
    assert r.status_code == 200
    uid = r.json()["uuid"]
    nested = {"level1": {"list": [1, 2, {"k": "v"}], "empty": {}}, "num": 0}
    payload = {"uuid": uid, "category": "analyzer", "properties": nested, "cookie": None}
    r2 = client.post("/properties", json=payload)
    assert r2.status_code == 200
    out = r2.json()
    assert out.get("properties") == nested
    assert "cookie" in out and out["cookie"] is None

def test_get_properties_unknown_uuid(client):
    bad_uuid = str(uuid.uuid4())
    r = client.get("/properties", params={"uuid": bad_uuid})
    assert r.status_code == 404

def test_get_properties_after_update(client, rand_name):
    r1 = client.post("/register", json={"category": "semantic_attribute", "name": rand_name, "description": "x"})
    assert r1.status_code == 200
    uid = r1.json()["uuid"]
    props = {"p1": True}
    payload = {"uuid": uid, "category": "semantic_attribute", "properties": props, "cookie": {"c": 1}}
    r2 = client.post("/properties", json=payload)
    assert r2.status_code == 200
    out2 = r2.json()
    assert out2.get("properties") == props
    assert out2.get("cookie") == {"c": 1}
    # GET back
    r3 = client.get("/properties", params={"uuid": uid})
    assert r3.status_code == 200
    out3 = r3.json()
    assert out3.get("properties") == props
    assert out3.get("cookie") == {"c": 1}
    ts = out3.get("updated_at")
    assert ts and re.match(r".*(Z|\+00:00)$", ts)
    dt = parse_iso_datetime(ts)
    assert dt.tzinfo is not None

def test_updated_at_changes_on_update(client, rand_name):
    r = client.post("/register", json={"category": "storage_layer", "name": rand_name, "description": "x"})
    assert r.status_code == 200
    uid = r.json()["uuid"]
    payload = {"uuid": uid, "category": "storage_layer", "properties": {"a": 1}}
    r1 = client.post("/properties", json=payload)
    assert r1.status_code == 200
    t1 = parse_iso_datetime(r1.json().get("updated_at"))
    time.sleep(1)
    payload["properties"] = {"a": 2}
    r2 = client.post("/properties", json=payload)
    assert r2.status_code == 200
    t2 = parse_iso_datetime(r2.json().get("updated_at"))
    assert t2 > t1

def test_openapi_schema_contains_models(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    schemas = spec.get("components", {}).get("schemas", {})
    expected = [
        "RegisterRequest", "RegisterResponse", "ResolveResponse",
        "PropertiesRequest", "PropertiesResponse",
    ]
    for name in expected:
        assert name in schemas, f"Schema {name} missing"
    
def test_resolve_missing_query_params(client, rand_name):
    # Missing both category and name
    r = client.get("/resolve")
    assert r.status_code == 422
    # Missing category only
    r = client.get("/resolve", params={"name": rand_name})
    assert r.status_code == 422
    # Missing name only
    r = client.get("/resolve", params={"category": "analyzer"})
    assert r.status_code == 422

def test_resolve_cookie_default_none(client, rand_name):
    # Cookie should be None if not provided during registration
    category = "semantic_label"
    name = rand_name
    # Register without cookie
    r1 = client.post("/register", json={"category": category, "name": name, "description": "no cookie"})
    assert r1.status_code == 200
    # Resolve and check cookie
    r2 = client.get("/resolve", params={"category": category, "name": name})
    assert r2.status_code == 200
    res = r2.json()
    assert "cookie" in res and res["cookie"] is None

def test_get_properties_missing_uuid_param(client):
    # GET /properties without uuid should return validation error
    r = client.get("/properties")
    assert r.status_code == 422

def test_get_properties_invalid_uuid_format(client):
    # GET /properties with malformed uuid should return validation error
    r = client.get("/properties", params={"uuid": "not-a-uuid"})
    assert r.status_code == 422

def test_set_properties_invalid_properties_type(client, rand_name):
    # properties must be an object
    category = "analyzer"
    name = rand_name
    # Register entry first
    r1 = client.post("/register", json={"category": category, "name": name, "description": "desc"})
    assert r1.status_code == 200
    uid = r1.json()["uuid"]
    # properties not a dict
    r2 = client.post("/properties", json={"uuid": uid, "category": category, "properties": "not a dict"})
    assert r2.status_code == 422

def test_set_properties_invalid_cookie_type(client, rand_name):
    # cookie must be an object or null
    category = "analyzer"
    name = rand_name
    # Register entry first
    r1 = client.post("/register", json={"category": category, "name": name, "description": "desc"})
    assert r1.status_code == 200
    uid = r1.json()["uuid"]
    # cookie not a dict
    r2 = client.post("/properties", json={"uuid": uid, "category": category, "properties": {}, "cookie": "not a dict"})
    assert r2.status_code == 422

def test_set_properties_invalid_uuid_format(client):
    # POST /properties with malformed uuid should return validation error
    r = client.post("/properties", json={"uuid": "invalid-uuid", "category": "analyzer", "properties": {}})
    assert r.status_code == 422

def test_name_case_sensitivity(client, rand_name):
    # Names are case-sensitive
    category = "analyzer"
    base_name = rand_name
    mixed_name = base_name.upper()
    # Register with mixed case name
    r1 = client.post("/register", json={"category": category, "name": mixed_name, "description": "case test"})
    assert r1.status_code == 200
    # Resolve with exact case
    r2 = client.get("/resolve", params={"category": category, "name": mixed_name})
    assert r2.status_code == 200
    # Resolve with different case should not find it
    r3 = client.get("/resolve", params={"category": category, "name": base_name})
    assert r3.status_code == 404