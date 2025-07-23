from fastapi import APIRouter, HTTPException, status
from models import Profesor, CrearProfesor, ActualizarProfesor, Departamento
from db import SessionDep
from sqlmodel import select

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