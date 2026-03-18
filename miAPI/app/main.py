#importaciones 
from fastapi import FastAPI, APIRouter
from app.routers import usuarios, varios

#Instancia del servidor 
app= FastAPI(
    title="Mi Primer API",
    description="Fabiola Martinez Rauda",
    version="1.0"
)

app.include_router(usuarios.router)
app.include_router(varios.routerV)


