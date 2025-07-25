from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .profesor_model import Profesor

class DepartamentoBase(SQLModel):
    nombre: str = Field(..., max_length=30, description="Nombre del departamento")
    descripcion: str = Field(..., max_length=150, description="Descripción del departamento")

class CrearDepartamento(DepartamentoBase):
    pass

class ActualizarDepartamento(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=30, description="Nombre del departamento")
    descripcion: Optional[str] = Field(default=None, max_length=150, description="Descripción del departamento")

class Departamento(DepartamentoBase, table=True):
    __tablename__ = "departamentos"
    departamento_id: Optional[int] = Field(default=None, primary_key=True)
    profesores: list["Profesor"] = Relationship(back_populates="departamento", cascade_delete=True)