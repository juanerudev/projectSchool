from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from .departamento_model import Departamento

class ProfesorBase(SQLModel):
    nombre: str = Field(..., max_length=30, description="Nombre del profesor")
    apellido: str = Field(..., max_length=30, description="Apellido del profesor")
    email: EmailStr = Field(..., description="Email del profesor")
    departamento_id: int = Field(foreign_key="departamentos.departamento_id", description="ID del departamento")

class CrearProfesor(ProfesorBase):
    pass

class ActualizarProfesor(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=30, description="Nombre del profesor")
    apellido: Optional[str] = Field(default=None, max_length=30, description="Apellido del profesor")
    email: Optional[EmailStr] = Field(default=None, description="Email del profesor")
    departamento_id: Optional[int] = Field(default=None, foreign_key="departamentos.departamento_id", description="ID del departamento")

class Profesor(ProfesorBase, table=True):
    __tablename__ = "profesores"
    profesor_id: Optional[int] = Field(default=None, primary_key=True)
    departamento: Optional["Departamento"] = Relationship(back_populates="profesores")