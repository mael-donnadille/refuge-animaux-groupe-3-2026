from pydantic import BaseModel
from refuge_esn81.schemas.speciesSchema import Species

class AnimalBase(BaseModel):
    name: str
    # A compléter
    species_id: int

class AnimalCreate(AnimalBase):
    pass

class Animal(AnimalBase):
    id: int
    # A compléter
    species: Species

    class Config:
        from_attributes = True
