from surrealdb import Surreal
from config import (
    SURREALDB_URL,
    SURREALDB_USERNAME,
    SURREALDB_PASSWORD,
    SURREALDB_NAMESPACE,
    SURREALDB_DATABASE,
)

def get_db():
    db = Surreal(SURREALDB_URL)
    db.signin({"username": SURREALDB_USERNAME, "password": SURREALDB_PASSWORD})
    db.use(SURREALDB_NAMESPACE, SURREALDB_DATABASE)
    return db
