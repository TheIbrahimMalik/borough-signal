"""Make `apps/api/` importable so tests can `from services.X import Y`,
matching the runtime import style used by the FastAPI app and LangGraph nodes.
"""
import os
import sys

API_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if API_ROOT not in sys.path:
    sys.path.insert(0, API_ROOT)
