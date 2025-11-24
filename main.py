# main.py
from fastapi import FastAPI, Depends
import random # Importamos el módulo random
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# main.py (debajo de los imports)



#1 crear base de datos
DATABASE_URL = "sqlite:///./galletas.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# crear modelo base de datos, la tabla
class GalletaDB(Base):
    __tablename__ = "galletas"
    id = Column(Integer, primary_key=True, index=True)
    frase = Column(String)

# Modelo Pydantic para definir la estructura del body
class GalletaInput(BaseModel):
    frase: str

Base.metadata.create_all(bind=engine) # crear la tabla Y ARCHIVO

# 2. Creamos la aplicación FastAPI
app = FastAPI()

# 2. Creamos nuestro "frasco" (base de datos en memoria)
#    con frases predefinidas
'''
db_galletas = [
    "La paciencia es una virtud.",
    "El que madruga, Dios lo ayuda.",
    "No dejes para mañana lo que puedes hacer hoy."
]'''

#Acceder a BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Requisito del desafío: "iniciarla con 2 o 3 frases predefinidas"
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    # Si no hay galletas, agregamos las iniciales
    if db.query(GalletaDB).count() == 0:
        frases = [
            "La paciencia es una virtud.",
            "El que madruga, Dios lo ayuda.",
            "No dejes para mañana lo que puedes hacer hoy."
        ]
        for f in frases:
            db.add(GalletaDB(frase=f))
        db.commit()
        print("--- Frases iniciales cargadas en galletas.db ---")
    db.close()

#Consultar galleta    
@app.get("/consultar_galleta")
def consultar_galleta(db: Session = Depends(get_db)):
    # Traemos todas las galletas de la base de datos
    todas_las_galletas = db.query(GalletaDB).all()
    
    if not todas_las_galletas:
        return {"mensaje": "No hay galletas en el frasco."}
        
    # Elegimos una al azar [cite: 15]
    galleta_azar = random.choice(todas_las_galletas)
    return {"galleta": galleta_azar.frase} 

# POST: Agregar nueva galleta

@app.post("/agregar_galleta")
def agregar_galleta(galleta: GalletaInput, db: Session = Depends(get_db)):
    # Creamos el objeto para la base de datos
    nueva_galleta = GalletaDB(frase=galleta.frase)
    
    # Guardamos en la base de datos
    db.add(nueva_galleta)
    db.commit() # Confirmamos el guardado
    
    return {"mensaje": "¡Galleta agregada correctamente!"}