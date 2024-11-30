from pydantic import BaseModel, EmailStr
from typing import Optional

class SugerenciasDTO(BaseModel):
    id_usuario: int
    id_contenido: int
    razon: Optional[str]

    class Config:
        orm_mode = True
