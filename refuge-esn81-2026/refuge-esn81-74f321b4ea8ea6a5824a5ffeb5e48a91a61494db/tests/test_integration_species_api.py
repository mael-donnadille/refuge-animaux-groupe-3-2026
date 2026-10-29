"""Tests d'integration des routes /api/species (router + service + base)."""


def test_create_species_route(client):
    # Setup
    data = {"name": "Chat"}
    # Action
    response = client.post("/api/species/", json=data)
    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Chat"}


def test_list_species_route_empty(client):
    # Action
    response = client.get("/api/species/")
    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_species_route(client):
    # Setup
    client.post("/api/species/", json={"name": "Chat"})
    client.post("/api/species/", json={"name": "Chien"})
    # Action
    response = client.get("/api/species/")
    # Assert
    assert response.status_code == 200
    assert [s["name"] for s in response.json()] == ["Chat", "Chien"]


def test_create_species_route_missing_name(client):
    # Action
    response = client.post("/api/species/", json={})
    # Assert : FastAPI refuse les donnees invalides avec une 422
    assert response.status_code == 422
