import tempfile
import sqlite3
import pytest
from uuid import uuid4

import registry_service.service as service
from registry_service.models import RegisterRequest
from fastapi import HTTPException


def setup_db(tmp_path):
    # Override database path and initialize schema
    db_file = tmp_path / "registry.sqlite"
    service.db_path = str(db_file)
    service.startup()
    return sqlite3.connect(service.db_path)


def test_lookup_direct_existing(tmp_path):
    conn = setup_db(tmp_path)
    # Register entry directly via service.register
    req = RegisterRequest(
        category="semantic_label", name="direct_test", description="desc"
    )
    resp = service.register(req, conn)
    uid = resp.uuid
    # Direct lookup should return correct values
    lookup = service.lookup(uid, conn)
    assert lookup.uuid == uid
    assert lookup.category == "semantic_label"
    assert lookup.name == "direct_test"


def test_lookup_direct_missing(tmp_path):
    conn = setup_db(tmp_path)
    # Lookup unknown UUID should raise 404
    missing_uuid = uuid4()
    with pytest.raises(HTTPException) as exc:
        service.lookup(missing_uuid, conn)
    assert exc.value.status_code == 404