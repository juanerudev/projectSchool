from fastapi import APIRouter, HTTPException, status
from models import Estudiante, Asignatura
from db import SessionDep
from sqlmodel import select
from pydantic import BaseModel

router = APIRouter()

class InscripcionRequest(BaseModel):
    estudiante_id: int
    asignatura_id: int

@router.post("/inscribir", status_code=status.HTTP_201_CREATED)
async def inscribir_estudiante(session: SessionDep, inscripcion: InscripcionRequest):
    """Inscribir un estudiante en una asignatura"""
    
    # Verificar que el estudiante existe
    estudiante = session.get(Estudiante, inscripcion.estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar que la asignatura existe
    asignatura = session.get(Asignatura, inscripcion.asignatura_id)
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignatura no encontrada"
        )
    
    # Verificar si el estudiante ya está inscrito en la asignatura
    if asignatura in estudiante.asignaturas:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El estudiante ya está inscrito en esta asignatura"
        )
    
    # Inscribir estudiante en la asignatura
    estudiante.asignaturas.append(asignatura)
    session.add(estudiante)
    session.commit()
    
    return {
        "detail": "Estudiante inscrito exitosamente",
        "estudiante": f"{estudiante.nombre} {estudiante.apellido}",
        "asignatura": asignatura.nombre
    }

@router.delete("/desinscribir", status_code=status.HTTP_200_OK)
async def desinscribir_estudiante(session: SessionDep, inscripcion: InscripcionRequest):
    """Desinscribir un estudiante de una asignatura"""
    
    # Verificar que el estudiante existe
    estudiante = session.get(Estudiante, inscripcion.estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar que la asignatura existe
    asignatura = session.get(Asignatura, inscripcion.asignatura_id)
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignatura no encontrada"
        )
    
    # Verificar si el estudiante está inscrito en la asignatura
    if asignatura not in estudiante.asignaturas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El estudiante no está inscrito en esta asignatura"
        )
    
    # Desinscribir estudiante de la asignatura
    estudiante.asignaturas.remove(asignatura)
    session.add(estudiante)
    session.commit()
    
    return {
        "detail": "Estudiante desinscrito exitosamente",
        "estudiante": f"{estudiante.nombre} {estudiante.apellido}",
        "asignatura": asignatura.nombre
    }

@router.get("/estudiante/{estudiante_id}/asignaturas", response_model=list[Asignatura])
async def get_asignaturas_estudiante(session: SessionDep, estudiante_id: int):
    """Obtener todas las asignaturas de un estudiante"""
    
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    return estudiante.asignaturas

@router.get("/asignatura/{asignatura_id}/estudiantes", response_model=list[Estudiante])
async def get_estudiantes_asignatura(session: SessionDep, asignatura_id: int):
    """Obtener todos los estudiantes de una asignatura"""
    
    asignatura = session.get(Asignatura, asignatura_id)
    if not asignatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignatura no encontrada"
        )
    
    return asignatura.estudiantes