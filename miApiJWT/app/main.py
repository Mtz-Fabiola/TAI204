# importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Configuración JWT
SECRET_KEY = "FabiolaMtz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def crear_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verificar_peticion(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# Instancia del servidor
app = FastAPI(
    title="Mi Primer API",
    description="Fabiola Martinez Rauda",
    version="1.0"
)

# Tabla ficticia
usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 21},
    {"id": 2, "nombre": "Coral", "edad": 21},
    {"id": 3, "nombre": "Saul", "edad": 21},
]

# Modelo Pydantic de validacion
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanito Doe")
    edad: int = Field(..., ge=1, le=125, description="Edad valida entre 1 y 125")

# Endpoints tipo get
@app.get("/", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo", tags=['Asincronia'])
async def Hola():
    await asyncio.sleep(5)
    return {"mensaje": "Hola Mundo FastAPI", "status": "200"}

@app.get("/v1/ParametroOb/{id}", tags=['Parametro Obligatorio'])
async def Consultauno(id: int):
    return {"mensaje": "Usuario encontrado", "usuario": id, "status": "200"}

@app.get("/v1/ParametroOp/", tags=['Parametro Opcional'])
async def Consultados(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK}
        return {"mensaje": "usuario no encontrado", "status": 200}
    else:
        return {"mensaje": "No se proporciono id", "status": 200}

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def ConsultaT():
    return {"status": "200", "total": len(usuarios), "Usuarios": usuarios}

@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios.append(usuario.dict())
    return {"Mensaje": "Usuario agregado", "Usuario": usuario, "Status": "200"}

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario: dict, usuarioAuth: str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre")
            usr["edad"] = usuario.get("edad")
            return {"mensaje": "Usuario actualizado", "Usuario": usr, "Status": "200"}
    raise HTTPException(status_code=400, detail="El id no existe")

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {"Mensaje": f"Usuario eliminado por {usuarioAuth}"}
    raise HTTPException(status_code=400, detail="El id no existe")

# Endpoint para login y generar token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username != "admin" or password != "1234":
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}