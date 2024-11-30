from pydantic import BaseModel, EmailStr
from typing import Optional

class ComentariosDTO(BaseModel):
    id_usuario: int
    id_contenido: int
    puntaje: float
    comentario: Optional[str]

    class Config:
        orm_mode = True
