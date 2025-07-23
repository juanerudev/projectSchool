from fastapi import APIRouter, HTTPException, status
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