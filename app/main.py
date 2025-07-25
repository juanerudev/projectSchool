from fastapi import FastAPI
from routers import departamento_router, profesor_router, asignatura_router
from db import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(departamento_router.router, prefix="/api/v1/departamentos", tags=["departamentos"])
app.include_router(profesor_router.router, prefix="/api/v1/profesores", tags=["profesores"])
app.include_router(asignatura_router.router, prefix="/api/v1/asignaturas", tags=["asignaturas"])

@app.get("/")
async def root():
    return {"message":"Inicio"}