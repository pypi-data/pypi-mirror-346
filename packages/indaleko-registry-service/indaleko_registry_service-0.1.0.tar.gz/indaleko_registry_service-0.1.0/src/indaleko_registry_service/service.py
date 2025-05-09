from fastapi import FastAPI, HTTPException, Depends
from uuid import uuid4, UUID
from datetime import datetime, UTC
import sqlite3
import json

from .models import (
    RegisterRequest,
    RegisterResponse,
    ResolveResponse,
    PropertiesRequest,
    PropertiesResponse,
    LookupResponse,
)

app = FastAPI(title="Indaleko Registration Service", version="0.1")

# Path to SQLite database file; overrideable by tests
db_path = "registry.sqlite"

def get_db():
    """
    FastAPI dependency that yields a new SQLite connection per request.
    """
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

@app.on_event("startup")
def startup():
    """
    Initialize the database on application startup.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS registry_entries (
            uuid TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            schema TEXT,
            cookie TEXT,
            version INTEGER,
            registered_at TEXT,
            deprecated INTEGER
        )
        """
    )
    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_category_name ON registry_entries (category, name)
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS registry_properties (
            uuid TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            properties TEXT,
            cookie TEXT,
            updated_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

@app.post("/register", response_model=RegisterResponse)
def register(req: RegisterRequest, conn: sqlite3.Connection = Depends(get_db)):
    """Register a new entry with semantic category and name."""
    uid = str(uuid4())
    now = datetime.now(UTC).isoformat()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO registry_entries
            (uuid, category, name, description, schema, cookie, version, registered_at, deprecated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                uid,
                req.category.value,
                req.name,
                req.description,
                json.dumps(req.schema) if req.schema else None,
                json.dumps(req.cookie) if req.cookie else None,
                1,
                now,
                0,
            ),
        )
        conn.commit()
        return RegisterResponse(uuid=UUID(uid), registered_at=datetime.fromisoformat(now))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Duplicate name/category")

@app.get("/resolve", response_model=ResolveResponse)
def resolve(category: str, name: str, conn: sqlite3.Connection = Depends(get_db)):
    """Resolve a registered entry by category and name to its UUID."""
    cur = conn.cursor()
    cur.execute(
        "SELECT uuid, cookie FROM registry_entries WHERE category = ? AND name = ?",
        (category, name),
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Entry not found")
    return ResolveResponse(uuid=UUID(row[0]), cookie=json.loads(row[1]) if row[1] else None)

@app.post("/properties", response_model=PropertiesResponse)
def set_properties(req: PropertiesRequest, conn: sqlite3.Connection = Depends(get_db)):
    """Set or update properties for an existing registry entry."""
    now = datetime.now(UTC).isoformat()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM registry_entries WHERE uuid = ? AND category = ?",
        (str(req.uuid), req.category),
    )
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail=f"Registry entry not found for UUID {req.uuid}")
    cur.execute(
        """
        INSERT INTO registry_properties (uuid, category, properties, cookie, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(uuid) DO UPDATE SET
            properties = excluded.properties,
            cookie = excluded.cookie,
            updated_at = excluded.updated_at
        """,
        (
            str(req.uuid),
            req.category,
            json.dumps(req.properties),
            json.dumps(req.cookie) if req.cookie else None,
            now,
        ),
    )
    conn.commit()
    return PropertiesResponse(
        uuid=req.uuid,
        category=req.category,
        properties=req.properties,
        cookie=req.cookie,
        updated_at=datetime.fromisoformat(now),
    )

@app.get("/properties", response_model=PropertiesResponse)
def get_properties(uuid: UUID, conn: sqlite3.Connection = Depends(get_db)):
    """Retrieve properties for a given registry entry."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM registry_properties WHERE uuid = ?", (str(uuid),))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Properties not found")
    return PropertiesResponse(
        uuid=UUID(row[0]),
        category=row[1],
        properties=json.loads(row[2]),
        cookie=json.loads(row[3]) if row[3] else None,
        updated_at=datetime.fromisoformat(row[4]),
    )

@app.get("/lookup", response_model=LookupResponse)
def lookup(uuid: UUID, conn: sqlite3.Connection = Depends(get_db)):
    """Reverse lookup: retrieve category and name by UUID."""
    cur = conn.cursor()
    cur.execute(
        "SELECT uuid, category, name FROM registry_entries WHERE uuid = ?",
        (str(uuid),)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Entry not found for UUID {uuid}")
    return LookupResponse(
        uuid=UUID(row[0]),
        category=row[1],
        name=row[2],
    )