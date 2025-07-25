from fastapi import APIRouter, HTTPException, status, Query
from models import Estudiante, CrearEstudiante, ActualizarEstudiante
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/", response_model=Estudiante, status_code=status.HTTP_201_CREATED)
async def create_estudiante(session: SessionDep, estudiante_data: CrearEstudiante):
    # Verificar si ya existe un estudiante con ese email
    query_existe_email = select(Estudiante).where(Estudiante.email == estudiante_data.email)
    existe_email = session.exec(query_existe_email).first()

    if existe_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Ya existe un estudiante con ese email"
        )

    # Crear el nuevo estudiante
    estudiante_dict = estudiante_data.model_dump()
    estudiante_dict['nombre'] = estudiante_dict['nombre'].strip()
    estudiante_dict['apellido'] = estudiante_dict['apellido'].strip()
    nuevo_estudiante = Estudiante.model_validate(estudiante_dict)

    session.add(nuevo_estudiante)
    session.commit()
    session.refresh(nuevo_estudiante)
    return nuevo_estudiante

@router.get("/", response_model=list[Estudiante])
async def get_estudiantes(
    session: SessionDep, 
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=10)
):
    query = select(Estudiante).offset(skip).limit(limit).order_by(Estudiante.apellido, Estudiante.nombre)
    estudiantes = session.exec(query).all()
    return estudiantes

@router.get("/{estudiante_id}", response_model=Estudiante)
async def get_estudiante(session: SessionDep, estudiante_id: int):
    estudiante = session.get(Estudiante, estudiante_id)

    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Estudiante no encontrado"
        )
    
    return estudiante

@router.patch("/{estudiante_id}", response_model=Estudiante)
async def update_estudiante(session: SessionDep, estudiante_id: int, estudiante_data: ActualizarEstudiante):
    estudiante = session.get(Estudiante, estudiante_id)

    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Estudiante no encontrado"
        )
    
    # Verificar email único si se está actualizando
    if estudiante_data.email and estudiante_data.email != estudiante.email:
        existe_email = session.exec(select(Estudiante).where(Estudiante.email == estudiante_data.email)).first()

        if existe_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Ya existe un estudiante con ese email"
            )

    # Preparar datos para actualización
    estudiante_data_dict = estudiante_data.model_dump(exclude_unset=True)
    
    # Limpiar espacios en nombre y apellido si se proporcionan
    if 'nombre' in estudiante_data_dict:
        estudiante_data_dict['nombre'] = estudiante_data_dict['nombre'].strip()
    if 'apellido' in estudiante_data_dict:
        estudiante_data_dict['apellido'] = estudiante_data_dict['apellido'].strip()

    estudiante.sqlmodel_update(estudiante_data_dict)

    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.delete("/{estudiante_id}")
async def delete_estudiante(session: SessionDep, estudiante_id: int):
    estudiante = session.get(Estudiante, estudiante_id)

    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Estudiante no encontrado"
        )
    
    session.delete(estudiante)
    session.commit()
    return {"detail": "Estudiante eliminado correctamente"}