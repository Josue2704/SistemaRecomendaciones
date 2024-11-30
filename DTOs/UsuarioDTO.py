from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioDTO(BaseModel):
    nombre: str
    edad: Optional[int]
    nacionalidad: Optional[str]
    preferencias: Optional[dict]
    ubicacion: Optional[str]
    email: EmailStr
    fecha_registro: Optional[datetime]

class UsuarioCreateDTO(UsuarioDTO):
    contraseña: str

class UsuarioResponseDTO(UsuarioDTO):
    id_usuario: int
    fecha_registro: datetime

    class Config:
        from_attributes = True  # Reemplazado por from_attributes
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

