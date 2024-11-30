from sqlalchemy.orm import relationship
from Connection.database import Base
from sqlalchemy import Column, Integer, String, Text, Enum, Date, DECIMAL


class PeliculasSeries(Base):
    __tablename__ = "PeliculasSeries"

    id_contenido = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Confirmamos autoincremental
    nombre = Column(String(150), nullable=False)
    tipo = Column(Enum("Película", "Serie", name="tipo_enum"), nullable=False)  # Enum nombrado explícitamente
    valoracion_promedio = Column(DECIMAL(3, 2), default=0.0)
    genero = Column(String(100), nullable=False)
    visualizaciones = Column(Integer, default=0)  # Estadísticas, no relación
    fecha_estreno = Column(Date)
    trailer_url = Column(String(255))
    descripcion = Column(Text)
    duracion = Column(Integer)

    # Relaciones adicionales
    comentarios = relationship("Comentarios", back_populates="contenido")
    sugerencias = relationship("Sugerencias", back_populates="contenido")

    # Relación con Visualizaciones (corregida)
    visualizaciones_relacion = relationship(
        "Visualizaciones", back_populates="contenido"
    )

