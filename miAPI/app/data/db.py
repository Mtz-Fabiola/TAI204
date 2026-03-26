
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1. DEFINIMOS URL CONEXION
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
    )

# 2. CREAMOS EL MOTOR DE LA CONEXION
engine = create_engine(DATABASE_URL)

# 3. CREAMOS GESTION DE SESSIONES 
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

# 4. BASE DECLARATIVA PARA MODELO 
Base = declarative_base()

# 5. FUNCION QUE TRABAJA SESIONES CON LAS PETICIONES 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
