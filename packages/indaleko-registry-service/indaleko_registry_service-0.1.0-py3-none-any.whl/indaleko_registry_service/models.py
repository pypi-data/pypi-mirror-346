# models.py
import enum
from datetime import datetime, UTC
from uuid import UUID
from pydantic import BaseModel, AwareDatetime, field_validator

# -----------------------------
# Helpers
# -----------------------------


def _validate_timestamp(
    value: AwareDatetime,
) -> AwareDatetime:
    """Validate the timestamp."""
    if value is None:
        value = datetime.now(UTC)
    if isinstance(value, AwareDatetime) or isinstance(value, datetime):
        return value
    ts = datetime.fromisoformat(value)
    if not isinstance(ts, AwareDatetime):
        raise ValueError(f"Timestamp {ts} is not an AwareDatetime.")
    return ts


# -----------------------------
# API Models
# -----------------------------


class RegistrationCategory(enum.Enum):
    ACTIVITY_PROVIDER = "activity_provider"
    ANALYZER = "analyzer"
    LLM = "llm"
    MODEL_LABEL = "model_label"
    SEMANTIC_LABEL = "semantic_label"
    SEMANTIC_ATTRIBUTE = "semantic_attribute"
    STORAGE_LAYER = "storage_layer"

    @classmethod
    def list(cls):
        return [category.value for category in cls]


class RegisterRequest(BaseModel):
    category: RegistrationCategory
    name: str
    description: str
    schema: dict | None = None
    cookie: dict | None = None


class RegisterResponse(BaseModel):
    uuid: UUID
    registered_at: AwareDatetime

    @field_validator("registered_at", mode="before")
    @classmethod
    def validate_timestamp(
        cls: "RegistryEntry",
        value: AwareDatetime,
    ) -> AwareDatetime:
        return _validate_timestamp(value)


class ResolveResponse(BaseModel):
    uuid: UUID
    cookie: dict | None = None


class PropertiesRequest(BaseModel):
    uuid: UUID
    category: str
    properties: dict
    cookie: dict | None = None


class PropertiesResponse(BaseModel):
    uuid: UUID
    category: str
    properties: dict | None
    cookie: dict | None
    updated_at: AwareDatetime

    @field_validator("updated_at", mode="before")
    @classmethod
    def validate_timestamp(
        cls: "RegistryEntry",
        value: AwareDatetime,
    ) -> AwareDatetime:
        return _validate_timestamp(value)


# -----------------------------
# Internal Model
# -----------------------------


class RegistryEntry(BaseModel):
    uuid: UUID
    category: str
    name: str
    description: str
    schema: dict | None
    cookie: dict | None
    version: int
    registered_at: AwareDatetime
    deprecated: bool

    @field_validator("registered_at", mode="before")
    @classmethod
    def validate_timestamp(
        cls: "RegistryEntry",
        value: AwareDatetime,
    ) -> AwareDatetime:
        return _validate_timestamp(value)
