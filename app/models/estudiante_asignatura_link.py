from sqlmodel import SQLModel, Field
from typing import Optional

class EstudianteAsignaturaLink(SQLModel, table=True):
    __tablename__ = "estudiante_asignatura"
    
    estudiante_id: Optional[int] = Field(
        default=None, 
        foreign_key="estudiantes.estudiante_id", 
        primary_key=True
    )
    asignatura_id: Optional[int] = Field(
        default=None, 
        foreign_key="asignaturas.asignatura_id", 
        primary_key=True
    )