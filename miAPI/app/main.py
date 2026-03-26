#importaciones 
from fastapi import FastAPI, APIRouter
from app.routers import usuarios, varios
from app.data.db import engine
from app.data import usuario
from app.data.usuario import Usuario

usuario.Base.metadata.create_all(bind = engine)

#Instancia del servidor 
app= FastAPI(
    title="Mi Primer API",
    description="Fabiola Martinez Rauda",
    version="1.0"
)

# RUTAS DE ENDPOINTS
app.include_router(usuarios.router)
app.include_router(varios.routerV)


