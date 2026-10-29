"""Tests unitaires du service des animaux (AnimalService)."""

import pytest
from pydantic import ValidationError

from refuge_esn81.schemas.animalSchema import AnimalCreate
from refuge_esn81.schemas.speciesSchema import SpeciesCreate
from refuge_esn81.services.animalService import AnimalService
from refuge_esn81.services.specieService import SpecieService


def creer_espece(db, name="Chien"):
    """Cree une espece dans la base et la renvoie."""
    return SpecieService().create_specie(db, SpeciesCreate(name=name))


def donnees_animal(species_id):
    """Donnees valides pour creer un animal."""
    return {
        "name": "Nouk",
        "age": 3,
        "description": "Chien tres gentil",
        "gender": "male",
        "photo_url": "https://placedog.net/400",
        "species_id": species_id,
    }


def test_create_animal(db):
    # Setup
    service = AnimalService()
    espece = creer_espece(db)
    animal = AnimalCreate(**donnees_animal(espece.id))
    # Action
    result = service.create_animal(db, animal)
    # Assert
    assert result.id is not None
    assert result.name == "Nouk"
    assert result.age == 3
    assert result.gender == "male"
    assert result.species_id == espece.id


def test_create_animal_relation_species(db):
    # Setup
    service = AnimalService()
    espece = creer_espece(db, "Chat")
    animal = AnimalCreate(**donnees_animal(espece.id))
    # Action
    result = service.create_animal(db, animal)
    # Assert : la relation SQLAlchemy donne acces a l'espece
    assert result.species.name == "Chat"
    assert result in espece.animals


def test_get_animals_empty(db):
    # Setup
    service = AnimalService()
    # Action
    result = service.get_animals(db)
    # Assert
    assert result == []


def test_get_animals(db):
    # Setup
    service = AnimalService()
    espece = creer_espece(db)
    service.create_animal(db, AnimalCreate(**donnees_animal(espece.id)))
    service.create_animal(db, AnimalCreate(**{**donnees_animal(espece.id), "name": "Rex"}))
    # Action
    result = service.get_animals(db)
    # Assert
    assert [a.name for a in result] == ["Nouk", "Rex"]


def test_get_animals_skip_limit(db):
    # Setup
    service = AnimalService()
    espece = creer_espece(db)
    for name in ["A", "B", "C", "D"]:
        service.create_animal(db, AnimalCreate(**{**donnees_animal(espece.id), "name": name}))
    # Action
    result = service.get_animals(db, skip=1, limit=2)
    # Assert
    assert [a.name for a in result] == ["B", "C"]


def test_create_animal_age_type_error():
    # Setup
    data = {**donnees_animal(1), "age": "age_pas_un_nombre"}
    # Action
    with pytest.raises(ValidationError) as excinfo:
        AnimalCreate(**data)
    # Assert
    assert "age" in str(excinfo.value)


def test_create_animal_missing_field_error():
    # Setup
    data = donnees_animal(1)
    del data["name"]
    # Action
    with pytest.raises(ValidationError) as excinfo:
        AnimalCreate(**data)
    # Assert
    assert "name" in str(excinfo.value)
