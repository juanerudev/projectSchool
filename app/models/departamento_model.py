from sqlmodel import SQLModel, Field
from typing import Optional

class DepartamentoBase(SQLModel):
    nombre: str = Field(..., max_length=30, description="Nombre del departamento")
    descripcion: str = Field(..., max_length=150, description="Descripción del departamento")

class CrearDepartamento(DepartamentoBase):
    pass

class ActualizarDepartamento(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=30, description="Nombre del departamento")
    descripcion: Optional[str] = Field(default=None, max_length=150, description="Descripción del departamento")

class Departamento(DepartamentoBase):
    departamento_id: Optional[int] = Field(default=None)