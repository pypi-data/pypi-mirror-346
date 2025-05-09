"""
Command-line entrypoint for the registry-service package.
"""
import uvicorn

from .service import app

def main():
    """
    Run the FastAPI registry service using Uvicorn.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)