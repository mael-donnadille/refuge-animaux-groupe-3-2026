"""Tests unitaires du service des especes (SpecieService)."""

import pytest
from sqlalchemy.exc import IntegrityError

from refuge_esn81.schemas.speciesSchema import SpeciesCreate
from refuge_esn81.services.specieService import SpecieService


def test_create_specie(db):
    # Setup
    service = SpecieService()
    specie = SpeciesCreate(name="Chat")
    # Action
    result = service.create_specie(db, specie)
    # Assert
    assert result.id is not None
    assert result.name == "Chat"


def test_get_species_empty(db):
    # Setup
    service = SpecieService()
    # Action
    result = list(service.get_species(db))
    # Assert
    assert result == []


def test_get_species(db):
    # Setup
    service = SpecieService()
    service.create_specie(db, SpeciesCreate(name="Chat"))
    service.create_specie(db, SpeciesCreate(name="Chien"))
    expected_names = ["Chat", "Chien"]
    # Action
    result = list(service.get_species(db))
    # Assert
    assert [s.name for s in result] == expected_names


def test_get_species_limit(db):
    # Setup
    service = SpecieService()
    for name in ["Chat", "Chien", "Lapin"]:
        service.create_specie(db, SpeciesCreate(name=name))
    # Action
    result = list(service.get_species(db, limit=2))
    # Assert
    assert len(result) == 2


def test_create_specie_duplicate_name_error(db):
    # Setup
    service = SpecieService()
    service.create_specie(db, SpeciesCreate(name="Chat"))
    # Action
    with pytest.raises(IntegrityError):
        service.create_specie(db, SpeciesCreate(name="Chat"))
    # Assert : le nom d'une espece est unique, la base refuse le doublon
