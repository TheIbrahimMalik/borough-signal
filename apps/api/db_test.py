from surrealdb import Surreal
from config import (
    SURREALDB_URL,
    SURREALDB_USERNAME,
    SURREALDB_PASSWORD,
    SURREALDB_NAMESPACE,
    SURREALDB_DATABASE,
)

with Surreal(SURREALDB_URL) as db:
    db.use(SURREALDB_NAMESPACE, SURREALDB_DATABASE)
    db.signin({"username": SURREALDB_USERNAME, "password": SURREALDB_PASSWORD})

    print("AREAS")
    print(db.query("SELECT * FROM area;"))

    print("\nSEGMENTS")
    print(db.query("SELECT * FROM segment;"))

    print("\nISSUES")
    print(db.query("SELECT * FROM issue;"))

    print("\nEVIDENCE")
    print(db.query("SELECT * FROM evidence_doc;"))
