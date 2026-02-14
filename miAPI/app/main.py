#importaciones 
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
# OPTIONAL Especificar que podemos mandar parametros o no

#Instancia del servidor 
app= FastAPI(
    title="Mi Primer API",
    description="Fabiola Martinez Rauda",
    version="1.0"
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

@app.get("/v1/ParametroOb/{id}",tags=['Parametro Obligatorio'])
#{id} Se vuelve obligatorio
async def Consultauno(id:int):
    return {"mensaje":"Usuario encontrado",
            "usuario":id,
            "status":"200"
            }

@app.get("/v1/ParametroOp/",tags=['Parametro Opcional'])
async def Consultados(id:Optional[int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"]== id:
                return{"mensaje": "usuario encontrado","usuario":usuarioK}
        return{"mensaje": "usuario no encontrado", "status":200}        
    else:
        return {"mensaje": "No se proporciono id", "status":200}
    
@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def ConsultaT():
    return{
        "status":"200",
        "total":len(usuarios),
        "Usuarios":usuarios
    }

@app.post("/v1/usuarios/",tags=['CRUD HTTP'])
async def agregar_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code = 400,
                detail = "El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "Mensaje": "Usuario agregado",
        "Usuario": usuario,
        "Status" : "200"
    }    

@app.put ("/v1/usuarios/{id}",tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario:dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre")
            usr["edad"] = usuario.get("edad")
            return{
                "mensaje": "Usuario actualizado",
                "Usuario": usr,
                "Status": "200"
            }
    raise HTTPException(
        status_code = 400,
        detail = "El id no existe"
    )

@app.delete("/v1/usuarios/",tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
         usuarios.remove(usr)
         return{
            "Mensaje": "Usuario eliminado",
            "Usuario": usr,
            "Status": "200"
        }
    raise HTTPException(
        status_code = 400,
        detail = "El id no existe"
    )


