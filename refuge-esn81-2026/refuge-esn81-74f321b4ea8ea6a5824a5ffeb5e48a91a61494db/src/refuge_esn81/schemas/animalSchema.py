from pydantic import BaseModel
from refuge_esn81.schemas.speciesSchema import Species

class AnimalBase(BaseModel):
    name: str
    age: int
    description: str
    gender: str
    photo_url: str
    species_id: int

class AnimalCreate(AnimalBase):
    pass

class Animal(AnimalBase):
    id: int
    species: Species

    class Config:
        from_attributes = True
