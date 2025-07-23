from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class ProfesorBase(SQLModel):
    nombre: str = Field(..., max_length=30, description="Nombre del profesor")
    apellido: str = Field(..., max_length=30, description="Apellido del profesor")
    email: EmailStr = Field(..., description="Email del profesor")

class CrearProfesor(ProfesorBase):
    pass

class ActualizarProfesor(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=30, description="Nombre del profesor")
    descripcion: Optional[str] = Field(default=None, max_length=30, description="Apellido del profesor")
    email: Optional[EmailStr] = Field(default=None, description="Email del profesor")

class Profesor(ProfesorBase, table=True):
    __tablename__ = "profesores"
    profesor_id: Optional[int] = Field(default=None, primary_key=True)