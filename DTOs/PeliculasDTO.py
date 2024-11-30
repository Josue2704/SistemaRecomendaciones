from pydantic import BaseModel
from datetime import date
from typing import Optional

class PeliculasSeriesDTO(BaseModel):
    nombre: str
    tipo: str  # Puede ser "Película" o "Serie"
    valoracion_promedio: float
    genero: str
    visualizaciones: int
    fecha_estreno: Optional[date]
    trailer_url: Optional[str]
    descripcion: Optional[str]
    duracion: Optional[int]

    class Config:
        from_attributes = True

class PeliculasSeriesCreateDTO(PeliculasSeriesDTO):
    """
    DTO específico para la creación de contenido.
    Excluye `id_contenido` porque es autoincremental en la base de datos.
    """
    pass

class PeliculasSeriesResponseDTO(PeliculasSeriesDTO):
    """
    DTO para las respuestas de contenido.
    Incluye `id_contenido` porque se devuelve después de la creación.
    """
    id_contenido: int

    class Config:
        from_attributes = True
