from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# Crear el motor de base de datos (sin async)
engine = create_engine(settings.DATABASE_URL, echo=False)

# Crear la sesión (sin async)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir el modelo base
Base = declarative_base()

# Función para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear las tablas si no existen
def create_tables():
    Base.metadata.create_all(bind=engine)

def init_db():
    from app.core.init_data import seed_database
    with SessionLocal() as db:
        seed_database(db)