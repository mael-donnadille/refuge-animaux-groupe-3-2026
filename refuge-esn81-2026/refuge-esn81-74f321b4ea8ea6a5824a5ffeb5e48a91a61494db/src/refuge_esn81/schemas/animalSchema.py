from pydantic import BaseModel
from typing import Literal
from refuge_esn81.schemas.speciesSchema import Species


Gender = Literal["Mâle", "Femelle", "Inconnu"]


class AnimalBase(BaseModel):
    name: str
    age: int
    description: str
    gender: Gender
    photo_url: str
    species_id: int


class AnimalCreate(AnimalBase):
    pass


class Animal(AnimalBase):
    id: int
    species: Species

    class Config:
        from_attributes = True
