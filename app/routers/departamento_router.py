from fastapi import APIRouter, HTTPException, status, Query
from models import Departamento, CrearDepartamento, ActualizarDepartamento
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/", response_model=Departamento, status_code=status.HTTP_201_CREATED)
async def create_departamento(session: SessionDep, departamento_data: CrearDepartamento):
    query_existe_departamento = select(Departamento).where(Departamento.nombre == departamento_data.nombre.strip())
    existe_departamento = session.exec(query_existe_departamento).first()

    if existe_departamento:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un departamento con ese nombre")
    
    departamento_dict = departamento_data.model_dump()
    departamento_dict['nombre'] = departamento_dict['nombre'].strip()
    departamento = Departamento.model_validate(departamento_dict)
    
    session.add(departamento)
    session.commit()
    session.refresh(departamento)
    return departamento

@router.get("/", response_model=list[Departamento])
async def get_departamentos(
    session: SessionDep, 
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=10)
):
    query = select(Departamento).offset(skip).limit(limit).order_by(Departamento.nombre)
    departamentos = session.exec(query).all()
    return departamentos

@router.get("/{departamento_id}", response_model=Departamento)
async def get_departamento(session: SessionDep, departamento_id: int):
    departamento = session.get(Departamento, departamento_id)
    if not departamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento no encontrado")
    
    return departamento

@router.patch("/{departamento_id}", response_model=Departamento)
async def update_departamento(session: SessionDep, departamento_id: int, departamento_data: ActualizarDepartamento):
    departamento = session.get(Departamento, departamento_id)

    if not departamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento no encontrado")
    
    if departamento_data.nombre:
        nombre_nuevo = departamento_data.nombre.strip()

        if nombre_nuevo != departamento.nombre:
            existe_departamento = session.exec(select(Departamento).where(Departamento.nombre == nombre_nuevo)).first()

            if existe_departamento:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un departamento con ese nombre")
            
            departamento_data.nombre = nombre_nuevo
    
    departamento_data_dict = departamento_data.model_dump(exclude_unset=True)
    departamento.sqlmodel_update(departamento_data_dict)

    session.add(departamento)
    session.commit()
    session.refresh(departamento)
    return departamento

@router.delete("/{departamento_id}")
async def delete_departamento(session: SessionDep, departamento_id: int):
    departamento = session.get(Departamento, departamento_id)
    if not departamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento no encontrano")
    
    session.delete(departamento)
    session.commit()
    return {"detail": "Departamento eliminado correctamente"}