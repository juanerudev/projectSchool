from fastapi import APIRouter, HTTPException, status
from models import Profesor, CrearProfesor, ActualizarProfesor
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/", response_model=Profesor, status_code=status.HTTP_201_CREATED)
async def create_profesor(session: SessionDep, profesor_data: CrearProfesor):
    profesor_dict = profesor_data.model_dump()
    profesor_dict['nombre'] = profesor_dict['nombre'].strip()
    profesor = Profesor.model_validate(profesor_dict)
    
    session.add(profesor)
    session.commit()
    session.refresh(profesor)
    return profesor