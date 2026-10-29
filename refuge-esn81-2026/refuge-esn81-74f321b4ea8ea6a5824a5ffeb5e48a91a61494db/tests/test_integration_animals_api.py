"""Tests d'integration des routes /api/animals (router + service + base)."""

ANIMAL = {
    "name": "Nouk",
    "age": 3,
    "description": "Chien tres gentil",
    "gender": "male",
    "photo_url": "https://placedog.net/400",
    "species_id": 1,
}


def test_create_animal_route(client):
    # Setup
    client.post("/api/species/", json={"name": "Chien"})
    expected = {**ANIMAL, "id": 1, "species": {"id": 1, "name": "Chien"}}
    # Action
    response = client.post("/api/animals/", json=ANIMAL)
    # Assert
    assert response.status_code == 200
    assert response.json() == expected


def test_create_animal_route_unknown_species(client):
    # Setup : aucune espece en base
    # Action
    response = client.post("/api/animals/", json=ANIMAL)
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Espece introuvable"


def test_list_animals_route_empty(client):
    # Action
    response = client.get("/api/animals/")
    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_animals_route(client):
    # Setup
    client.post("/api/species/", json={"name": "Chien"})
    client.post("/api/animals/", json=ANIMAL)
    client.post("/api/animals/", json={**ANIMAL, "name": "Rex"})
    # Action
    response = client.get("/api/animals/")
    # Assert
    assert response.status_code == 200
    animaux = response.json()
    assert [a["name"] for a in animaux] == ["Nouk", "Rex"]
    assert animaux[0]["species"]["name"] == "Chien"


def test_create_animal_route_age_type_error(client):
    # Setup
    client.post("/api/species/", json={"name": "Chien"})
    data = {**ANIMAL, "age": "trois"}
    # Action
    response = client.post("/api/animals/", json=data)
    # Assert
    assert response.status_code == 422


def test_create_animal_route_missing_field(client):
    # Setup
    client.post("/api/species/", json={"name": "Chien"})
    data = {k: v for k, v in ANIMAL.items() if k != "species_id"}
    # Action
    response = client.post("/api/animals/", json=data)
    # Assert
    assert response.status_code == 422
