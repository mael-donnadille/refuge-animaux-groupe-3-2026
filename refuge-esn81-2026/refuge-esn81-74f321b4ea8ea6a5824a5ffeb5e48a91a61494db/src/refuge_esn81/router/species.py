from fastapi import APIRouter, FastAPI, Depends, HTTPException
from refuge_esn81.schemas.speciesSchema import Species, SpeciesCreate
from sqlalchemy.orm import Session
from refuge_esn81.database.database import get_db
from refuge_esn81.services.specieService import SpecieService


speciesRouter = APIRouter(prefix="/api/species", tags=["species"])

@speciesRouter.get("/", response_model=list[Species])
async def get_species(db: Session = Depends(get_db)):
    service = SpecieService()
    return service.get_species(db)

@speciesRouter.post("/", response_model=Species)
def create_new_species(specie: SpeciesCreate, db: Session = Depends(get_db)):
    service = SpecieService()
    return service.create_specie(db, specie)