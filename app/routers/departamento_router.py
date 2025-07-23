from fastapi import APIRouter, HTTPException, status
from models import Departamento, CrearDepartamento, ActualizarDepartamento

router = APIRouter()

@router.post("/", response_model=Departamento, status_code=status.HTTP_201_CREATED)
async def create_departamento(departamento_data: CrearDepartamento):
    return departamento_data