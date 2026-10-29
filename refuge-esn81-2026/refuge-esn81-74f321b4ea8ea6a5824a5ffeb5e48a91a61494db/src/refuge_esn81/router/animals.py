from fastapi import APIRouter, FastAPI, Depends, HTTPException


animalsRouter = APIRouter(prefix="/animals", tags=["animals"])

# A compléter