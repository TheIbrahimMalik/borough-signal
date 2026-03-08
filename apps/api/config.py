import os
from dotenv import load_dotenv

load_dotenv()

SURREALDB_URL = os.getenv("SURREALDB_URL", "ws://localhost:8000")
SURREALDB_USERNAME = os.getenv("SURREALDB_USERNAME", "root")
SURREALDB_PASSWORD = os.getenv("SURREALDB_PASSWORD", "root")
SURREALDB_NAMESPACE = os.getenv("SURREALDB_NAMESPACE", "boroughsignal")
SURREALDB_DATABASE = os.getenv("SURREALDB_DATABASE", "main")
