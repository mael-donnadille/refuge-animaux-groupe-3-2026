import uvicorn

from fastapi import FastAPI
from refuge_esn81.router.animals import animalsRouter
from refuge_esn81.router.species import speciesRouter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(animalsRouter)
app.include_router(speciesRouter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, port=9000)
