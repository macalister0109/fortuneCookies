# main.py
from fastapi import FastAPI
import random # Importamos el módulo random
# main.py (al inicio del archivo)
from fastapi import FastAPI
import random
from pydantic import BaseModel # 👈 Importamos BaseModel

# main.py (debajo de los imports)

# Modelo Pydantic para definir la estructura del body
class Galleta(BaseModel):
    frase: str

# 1. Creamos la aplicación FastAPI
app = FastAPI()

# 2. Creamos nuestro "frasco" (base de datos en memoria)
#    con frases predefinidas
db_galletas = [
    "La paciencia es una virtud.",
    "El que madruga, Dios lo ayuda.",
    "No dejes para mañana lo que puedes hacer hoy."
]


# 3. Endpoint GET para consultar una galleta
@app.get("/consultar_galleta")
def consultar_galleta():
    # Elegimos una galleta (frase) al azar de nuestra lista
    galleta_elegida = random.choice(db_galletas)

    # Devolvemos la galleta en el formato pedido
    return {"galleta": galleta_elegida}

# 4. Endpoint POST para agregar una galleta
@app.post("/agregar_galleta")
def agregar_galleta(galleta: Galleta):
    # Agregamos la frase de la galleta recibida a nuestra lista
    db_galletas.append(galleta.frase)

    # Devolvemos el mensaje de éxito
    return {"mensaje": "¡Galleta agregada correctamente!"}