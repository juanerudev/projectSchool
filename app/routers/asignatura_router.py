from fastapi import APIRouter, HTTPException, status, Query
from models import Asignatura, CrearAsignatura, ActualizarAsignatura, Profesor
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/", response_model=Asignatura, status_code=status.HTTP_201_CREATED)
async def create_asignatura(session: SessionDep, asignatura_data: CrearAsignatura):
    query_existe_asignatura = select(Asignatura).where(Asignatura.nombre == asignatura_data.nombre.strip())
    existe_asignatura = session.exec(query_existe_asignatura).first()

    if existe_asignatura:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe una asignatura con ese nombre")
    
    if asignatura_data.profesor_id is not None:
        profesor = session.get(Profesor, asignatura_data.profesor_id)

        if not profesor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El profesor especificado no existe")


    asignatura_dict = asignatura_data.model_dump()
    asignatura_dict['nombre'] = asignatura_dict['nombre'].strip()
    nueva_asignatura = Asignatura.model_validate(asignatura_dict)

    session.add(nueva_asignatura)
    session.commit()
    session.refresh(nueva_asignatura)
    return nueva_asignatura

@router.get("/", response_model=list[Asignatura])
async def get_asignaturas(
    session: SessionDep, 
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=10)
):
    query = select(Asignatura).offset(skip).limit(limit).order_by(Asignatura.nombre)
    asignaturas = session.exec(query).all()
    return asignaturas

@router.get("/{asignatura_id}", response_model=Asignatura)
async def get_asignatura(session: SessionDep, asignatura_id: int):
    asignatura = session.get(Asignatura, asignatura_id)

    if not asignatura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
    
    return asignatura

@router.patch("/{asignatura_id}", response_model=Asignatura)
async def update_asignatura(session: SessionDep, asignatura_id: int, asignatura_data: ActualizarAsignatura):
    asignatura = session.get(Asignatura, asignatura_id)

    if not asignatura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
    
    if asignatura_data.nombre:
        nombre_nuevo = asignatura_data.nombre.strip()

        if nombre_nuevo != asignatura.nombre:
            existe_asignatura = session.exec(select(Asignatura).where(Asignatura.nombre == nombre_nuevo)).first()

            if existe_asignatura:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe una asignatura con ese nombre")
            
            asignatura_data.nombre = nombre_nuevo

    if asignatura_data.profesor_id is not None:
        profesor = session.get(Profesor, asignatura_data.profesor_id)

        if not profesor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El profesor especificado no existe")
    
    asignatura_data_dict = asignatura_data.model_dump(exclude_unset=True)
    asignatura.sqlmodel_update(asignatura_data_dict)

    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)
    return asignatura

@router.delete("/{asignatura_id}")
async def delete_asignatura(session: SessionDep, asignatura_id: int):
    asignatura = session.get(Asignatura, asignatura_id)

    if not asignatura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignatura no encontrada")
    
    session.delete(asignatura)
    session.commit()
    return {"detail":"Asignatura eliminada correctamente"}