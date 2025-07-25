from fastapi import FastAPI
from routers import departamento_router, profesor_router, asignatura_router, estudiante_router, inscripcion_router
from db import lifespan

app = FastAPI(
    title="API Gestión Académica",
    description="API para gestión de departamentos, profesores, asignaturas y estudiantes",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(departamento_router.router, prefix="/api/v1/departamentos", tags=["departamentos"])
app.include_router(profesor_router.router, prefix="/api/v1/profesores", tags=["profesores"])
app.include_router(asignatura_router.router, prefix="/api/v1/asignaturas", tags=["asignaturas"])
app.include_router(estudiante_router.router, prefix="/api/v1/estudiantes", tags=["estudiantes"])
app.include_router(inscripcion_router.router, prefix="/api/v1/inscripciones", tags=["inscripciones"])

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "API Gestión Académica",
        "version": "1.0.0",
        "docs": "/docs"
    }