from fastapi import APIRouter, HTTPException, status, Query
from models import Profesor, CrearProfesor, ActualizarProfesor, Departamento, Asignatura
from db import SessionDep
from sqlmodel import select
from typing import Optional

router = APIRouter()

@router.post("/", response_model=Profesor, status_code=status.HTTP_201_CREATED)
async def create_profesor(session: SessionDep, profesor_data: CrearProfesor):
    existe_email = session.exec(select(Profesor).where(Profesor.email == profesor_data.email)).first()

    if existe_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un profesor con ese email")
    
    departamento = session.get(Departamento, profesor_data.departamento_id)

    if not departamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El departamento especificado no existe")

    profesor_dict = profesor_data.model_dump()
    profesor_dict['nombre'] = profesor_dict['nombre'].strip()
    profesor = Profesor.model_validate(profesor_dict)
    
    session.add(profesor)
    session.commit()
    session.refresh(profesor)
    return profesor

@router.get("/", response_model=list[Profesor])
async def get_profesor(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=10),
    departamento_id: Optional[int] = Query(None, description="Filtrar profesores por departamento")
):
    query = select(Profesor).offset(skip).limit(limit)

    if departamento_id is not None:
        query = query.where(Profesor.departamento_id == departamento_id)
    
    query = query.order_by(Profesor.nombre)
    profesores = session.exec(query).all()
    return profesores

@router.get("/{profesor_id}", response_model=Profesor)
async def get_profesor(session: SessionDep, profesor_id: int):
    profesor = session.get(Profesor, profesor_id)

    if not profesor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    
    return profesor

@router.patch("/{profesor_id}", response_model=Profesor)
async def update_profesor(session: SessionDep, profesor_id: int, profesor_data: ActualizarProfesor):
    profesor = session.get(Profesor, profesor_id)

    if not profesor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    
    if profesor_data.email and profesor_data.email != profesor.email:
        existe_email = session.exec(select(Profesor).where(Profesor.email == profesor_data.email)).first()

        if existe_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un profesor con ese email")
    
    if profesor_data.departamento_id is not None:
        departamento = session.get(Departamento, profesor_data.departamento_id)
        if not departamento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El departamento especificado no existe")

    profesor_data_dict = profesor_data.model_dump(exclude_unset=True)
    profesor.sqlmodel_update(profesor_data_dict)

    session.add(profesor)
    session.commit()
    session.refresh(profesor)
    return profesor





@router.delete("/{profesor_id}")
async def delete_profesor(session: SessionDep, profesor_id: int):
    profesor = session.get(Profesor, profesor_id)

    if not profesor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    
    asignaturas = session.exec(select(Asignatura).where(Asignatura.profesor_id == profesor_id)).all()
    for asignatura in asignaturas:
        asignatura.profesor_id = None
        session.add(asignatura)
    session.commit()

    session.delete(profesor)
    session.commit()
    return {"detail":"Profesor eliminado correctamente"}