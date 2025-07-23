from fastapi import FastAPI
from routers import departamento_router
from db import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(departamento_router.router, prefix="/api/v1/departamentos", tags=["departamentos"])

@app.get("/")
async def root():
    return {"message":"Inicio"}