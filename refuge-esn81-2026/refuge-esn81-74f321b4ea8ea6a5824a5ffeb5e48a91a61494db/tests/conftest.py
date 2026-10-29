"""Configuration commune a tous les tests.

Les tests utilisent une base SQLite en memoire :
pas besoin de MySQL, et chaque test repart d'une base vide.
"""

import os

# database.py lit DATABASE_URL des l'import : on la definit avant tout
os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from refuge_esn81.database.database import Base, get_db
from refuge_esn81.main import app
from refuge_esn81.models.animal import Animal  # noqa: F401 (cree la table)
from refuge_esn81.models.species import Species  # noqa: F401 (cree la table)


@pytest.fixture
def db():
    """Session sur une base SQLite vide, detruite apres le test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def client(db):
    """Client de test de l'API, branche sur la base SQLite."""
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()
