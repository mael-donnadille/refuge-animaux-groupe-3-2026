from sqlalchemy.orm import Session
from refuge_esn81.schemas.speciesSchema import SpeciesCreate
from refuge_esn81.models.species import Species

class SpecieService:
    def create_specie(self, db: Session, specie: SpeciesCreate):
        db_specie = Species(name=specie.name)
        db.add(db_specie)
        db.commit()
        db.refresh(db_specie)
        return db_specie

    def get_species(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Species).offset(skip).limit(limit)