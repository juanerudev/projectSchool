from .departamento_model import Departamento, CrearDepartamento, ActualizarDepartamento
from .profesor_model import Profesor, CrearProfesor, ActualizarProfesor
from .asignatura_model import Asignatura, CrearAsignatura, ActualizarAsignatura
from .estudiante_model import Estudiante, CrearEstudiante, ActualizarEstudiante
from .estudiante_asignatura_link import EstudianteAsignaturaLink

__all__ = [
    "Departamento", 
    "CrearDepartamento", 
    "ActualizarDepartamento", 
    "Profesor", 
    "CrearProfesor", 
    "ActualizarProfesor",
    "Asignatura",
    "CrearAsignatura",
    "ActualizarAsignatura",
    "Estudiante",
    "CrearEstudiante",
    "ActualizarEstudiante",
    "EstudianteAsignaturaLink"
]