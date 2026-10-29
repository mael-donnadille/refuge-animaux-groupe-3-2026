import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite://")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from refuge_esn81.database.database import Base, get_db
from refuge_esn81.main import app
from refuge_esn81.models import Animal, Species


class RefugeApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.engine
        )
        Base.metadata.create_all(bind=cls.engine)

        def override_get_db():
            db = cls.session_factory()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=cls.engine)
        cls.engine.dispose()

    def setUp(self):
        with self.session_factory() as db:
            db.query(Animal).delete()
            db.query(Species).delete()
            db.commit()

    def test_species_can_be_created_and_listed(self):
        response = self.client.post(
            "/api/species/", json={"name": "Chien"}
        )

        self.assertEqual(response.status_code, 200)
        species = response.json()
        self.assertEqual(species["name"], "Chien")
        self.assertIsInstance(species["id"], int)

        response = self.client.get("/api/species/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [species])

    def test_animal_can_be_created_and_listed_with_its_species(self):
        species_response = self.client.post(
            "/api/species/", json={"name": "Chat"}
        )
        species = species_response.json()

        animal_payload = {
            "name": "Minou",
            "age": 3,
            "description": "Un chat calme",
            "gender": "Femelle",
            "photo_url": "https://example.com/minou.jpg",
            "species_id": species["id"],
        }
        response = self.client.post("/api/animals/", json=animal_payload)

        self.assertEqual(response.status_code, 200)
        animal = response.json()
        self.assertEqual(animal["name"], animal_payload["name"])
        self.assertEqual(animal["age"], animal_payload["age"])
        self.assertEqual(animal["description"], animal_payload["description"])
        self.assertEqual(animal["gender"], animal_payload["gender"])
        self.assertEqual(animal["photo_url"], animal_payload["photo_url"])
        self.assertEqual(animal["species"], species)

        response = self.client.get("/api/animals/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [animal])

    def test_animal_rejects_gender_outside_frontend_options(self):
        response = self.client.post(
            "/api/animals/",
            json={
                "name": "Rex",
                "age": 4,
                "description": "",
                "gender": "Autre",
                "photo_url": "",
                "species_id": 1,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_frontend_origin_is_allowed_by_cors(self):
        response = self.client.options(
            "/api/species/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            "http://localhost:3000",
        )


if __name__ == "__main__":
    unittest.main()
