"""Pytest fixtures: isolated SQLite test database + API test client.

Tests run from the REPO ROOT. The backend package is added to sys.path and
all file paths are absolute so results do not depend on the working directory.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))          # <project>/tests
PROJECT_ROOT = os.path.dirname(ROOT)                          # <project>/
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
sys.path.insert(0, BACKEND_DIR)

TEST_DB = os.path.join(BACKEND_DIR, "data", "test_citrusguard.db")
UPLOAD_DIR = os.path.join(BACKEND_DIR, "data", "uploads")

# Must be set BEFORE any app import (engine/settings read env at import time).
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["UPLOAD_DIR"] = UPLOAD_DIR

import pytest
from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.database.engine import Base, SessionLocal, engine, get_db
from app.main import app
from app.models import Orchard, OrchardZone, User


@pytest.fixture(scope="session", autouse=True)
def _create_schema():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    """Function-scoped session with a clean, minimally seeded database."""
    session = SessionLocal()
    # Wipe all tables.
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    # Seed demo users.
    session.add_all(
        [
            User(username="farmer", password_hash=hash_password("farmer123"),
                 role="farmer", full_name="Test Farmer"),
            User(username="operator", password_hash=hash_password("operator123"),
                 role="operator", full_name="Test Operator"),
        ]
    )
    # Seed one orchard with 8 zones (A-H).
    orchard = Orchard(name="Test Orchard", location="Vidarbha", area=50.0,
                      crop="Orange (Nagpur Santra)")
    session.add(orchard)
    session.flush()
    for i, name in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
        session.add(
            OrchardZone(
                orchard_id=orchard.id,
                zone_name=name,
                area=6.25,
                latitude=21.14 + i * 0.001,
                longitude=79.08 + i * 0.001,
                health_status="Healthy",
                risk_score=10.0,
            )
        )
    session.commit()
    yield session
    session.close()


@pytest.fixture()
def client(db):
    """TestClient with get_db overridden to use the test database."""
    def override():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    r = client.post("/auth/login", json={"username": "farmer", "password": "farmer123"})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
