from pydantic import BaseModel, Field

# Modelo Pydantic de validacion 
class crear_usuario(BaseModel):
    nombre: str = Field (..., min_lenhgt = 3, max_lenhgt = 50, example = "Juanito Doe")
    edad: int = Field (..., ge = 1, le = 125, description = "Edad valida entre 1 y 125" )

