from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from contextlib import asynccontextmanager
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la base de datos
DATABASE_DIR = "app/data"
os.makedirs(DATABASE_DIR, exist_ok=True)

sqlite_name = f"{DATABASE_DIR}/db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

# Configuración del engine con opciones mejoradas
engine = create_engine(
    sqlite_url,
    echo=False,  # Cambiar a True para debug
    connect_args={
        "check_same_thread": False,
        "timeout": 20  # Timeout para evitar locks prolongados
    },
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    pool_recycle=300     # Reciclar conexiones cada 5 minutos
)


def create_tables():
    """Crear todas las tablas"""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Tablas de base de datos creadas exitosamente")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        raise


@asynccontextmanager
async def lifespan(app):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("Iniciando aplicación...")
    create_tables()
    logger.info("Aplicación iniciada correctamente")
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación...")
    engine.dispose()
    logger.info("Aplicación cerrada correctamente")


def get_session():
    """Obtener sesión de base de datos con manejo de errores mejorado"""
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Error en la sesión de base de datos: {e}")
        raise


SessionDep = Annotated[Session, Depends(get_session)]