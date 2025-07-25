from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from .estudiante_asignatura_link import EstudianteAsignaturaLink

if TYPE_CHECKING:
    from .profesor_model import Profesor
    from .estudiante_model import Estudiante

class AsignaturaBase(SQLModel):
    nombre: str = Field(..., max_length=50, description="Nombre de la asignatura")
    descripcion: Optional[str] = Field(default=None, max_length=150, description="Descripción de la asignatura")
    profesor_id: Optional[int] = Field(default=None, foreign_key="profesores.profesor_id", description="ID del profesor")
    
class CrearAsignatura(AsignaturaBase):
    pass

class ActualizarAsignatura(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=50, description="Nombre de la asignatura")
    descripcion: Optional[str] = Field(default=None, max_length=150, description="Descripción de la asignatura")
    profesor_id: Optional[int] = Field(default=None, foreign_key="profesores.profesor_id", description="ID del profesor")

class Asignatura(AsignaturaBase, table=True):
    __tablename__ = "asignaturas"
    asignatura_id: Optional[int] = Field(default=None, primary_key=True)

    profesor: Optional["Profesor"] = Relationship(back_populates="asignaturas")
    estudiantes: list["Estudiante"] = Relationship(
        back_populates="asignaturas", 
        link_model=EstudianteAsignaturaLink
    )