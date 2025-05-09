"""
registry_service package: FastAPI app and data models for the registry service.
"""
from .service import app, db_path, get_db, startup

__all__ = ["app", "db_path", "get_db", "startup"]