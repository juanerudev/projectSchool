from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr
from .estudiante_asignatura_link import EstudianteAsignaturaLink

if TYPE_CHECKING:
    from .asignatura_model import Asignatura

class EstudianteBase(SQLModel):
    nombre: str = Field(..., max_length=30, description="Nombre del estudiante")
    apellido: str = Field(..., max_length=30, description="Apellido del estudiante")
    email: EmailStr = Field(..., description="Email del estudiante")

class CrearEstudiante(EstudianteBase):
    pass

class ActualizarEstudiante(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=30, description="Nombre del estudiante")
    apellido: Optional[str] = Field(default=None, max_length=30, description="Apellido del estudiante")
    email: Optional[EmailStr] = Field(default=None, description="Email del estudiante")

class Estudiante(EstudianteBase, table=True):
    __tablename__ = "estudiantes"
    estudiante_id: Optional[int] = Field(default=None, primary_key=True)
    
    asignaturas: list["Asignatura"] = Relationship(
        back_populates="estudiantes", 
        link_model=EstudianteAsignaturaLink
    )