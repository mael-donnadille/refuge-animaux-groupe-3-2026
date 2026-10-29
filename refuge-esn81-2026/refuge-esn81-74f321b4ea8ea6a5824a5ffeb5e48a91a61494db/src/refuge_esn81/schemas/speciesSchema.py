from pydantic import BaseModel

class SpeciesBase(BaseModel):
    name: str

class SpeciesCreate(SpeciesBase):
    pass

class Species(SpeciesBase):
    id: int

    class Config:
        from_attributes = True