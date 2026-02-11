#importaciones 
from fastapi import FastAPI
import asyncio
from typing import Optional
# OPTIONAL Especificar que podemos mandar parametros o no

#Instancia del servidor 
app= FastAPI(
    title="Mi Primer API",
    description="Fabiola Martinez Rauda",
    vesion="1.0"
)

#Tabla ficticia
usuarios=[
    {"id":1,"nombre":"Diego", "edad":21},
    {"id":2,"nombre":"Coral", "edad":21},
    {"id":3,"nombre":"Saul", "edad":21},
]

#Endpoints tipo get 
@app.get("/",tags=['Inicio'])
async def bienvenido ():
    return {"mensaje":"Bienvenido a FastAPI"}
# ejemplo  {"Correo":"fm0560240@gmail.com"}

@app.get("/holaMundo", tags=['Asincronia'])
async def Hola ():
    await asyncio.sleep(5) #peticion, consultaBD, Archivo
    return {
        "mensaje":"Hola Mundo FastAPI",
        "status":"200"
        }

@app.get("/v1/usuario/{id}",tags=['Parametro Obligatorio'])
#{id} Se vuelve obligatorio
async def Consultauno(id:int):
    return {"mensaje":"Usuario encontrado",
            "usuario":id,
            "status":"200"
            }

@app.get("/v1/usuarios/",tags=['Parametro Opcional'])
async def Consultados(id:Optional[int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"]== id:
                return{"mensaje": "usuario encontrado","usuario":usuarioK}
        return{"mensaje": "usuario no encontrado", "status":200}        
    else:
        return {"mensaje": "No se proporciono id", "status":200}