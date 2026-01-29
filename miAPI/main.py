#importaciones 
from fastapi import FastAPI
import asyncio

#Instancia del servidor 
app= FastAPI()

#Endpoints 
@app.get("/")
async def bienvenido ():
    return {"mensaje":"Bienvenido a FastAPI"}
# ejemplo  {"Correo":"fm0560240@gmail.com"}

@app.get("/holaMundo")
async def Hola ():
    await asyncio.sleep(5) #peticion, consultaBD, Archivo
    return {
        "mensaje":"Hola Mundo FastAPI",
        "status":"200"
        }

