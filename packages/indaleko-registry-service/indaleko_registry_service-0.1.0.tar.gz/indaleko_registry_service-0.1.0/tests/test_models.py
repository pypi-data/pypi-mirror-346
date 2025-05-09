import pytest
from datetime import datetime, UTC

import registry_service.models as models


def test_validate_timestamp_none():
    # None input should yield current time with timezone
    dt = models._validate_timestamp(None)
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None


def test_validate_timestamp_valid_string():
    # ISO string with timezone
    ts = "2025-05-05T12:00:00+00:00"
    dt = models._validate_timestamp(ts)
    assert isinstance(dt, datetime)
    assert dt.isoformat() == ts


def test_validate_timestamp_invalid_string():
    # ISO string without timezone should fail
    ts = "2025-05-05T12:00:00"
    with pytest.raises(ValueError):
        models._validate_timestamp(ts)


def test_registration_category_list():
    # Ensure all enum values are listed
    expected = [e.value for e in models.RegistrationCategory]
    assert models.RegistrationCategory.list() == expected
    
def test_registry_entry_timestamp_validator():
    # Test that RegistryEntry accepts ISO string timestamp
    from uuid import uuid4
    from registry_service.models import RegistryEntry

    ts = "2025-05-05T12:00:00+00:00"
    entry = RegistryEntry(
        uuid=uuid4(),
        category="analyzer", name="n", description="d",
        schema={}, cookie={}, version=1,
        registered_at=ts, deprecated=False
    )
    # Should parse and preserve timestamp
    assert entry.registered_at.isoformat() == ts