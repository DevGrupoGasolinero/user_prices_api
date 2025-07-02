from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()
DATA_FILE = "data.json"

# Modelo de entrada
class Gasolinera(BaseModel):
    archivo: str
    nombre: str

# Funciones de ayuda
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Endpoints
#@app.get("/")
#def read_all():
    #return load_data()

@app.get("/{key}")
def read_item(key: str):
    data = load_data()
    if key in data:
        return data[key]
    else:
        raise HTTPException(status_code=404, detail="No encontrado")

@app.post("/{key}")
def create_item(key: str, gasolinera: Gasolinera):
    data = load_data()
    if key in data:
        raise HTTPException(status_code=400, detail="Ya existe")
    data[key] = gasolinera.dict()
    save_data(data)
    return {"msg": "Creado", "data": data[key]}

@app.put("/{key}")
def update_item(key: str, gasolinera: Gasolinera):
    data = load_data()
    if key not in data:
        raise HTTPException(status_code=404, detail="No existe")
    data[key] = gasolinera.dict()
    save_data(data)
    return {"msg": "Actualizado", "data": data[key]}

@app.delete("/{key}")
def delete_item(key: str):
    data = load_data()
    if key not in data:
        raise HTTPException(status_code=404, detail="No existe")
    del data[key]
    save_data(data)
    return {"msg": "Eliminado"}
