from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Connection.database import Base

class Visualizaciones(Base):
    __tablename__ = "Visualizaciones"

    id_visualizacion = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    id_contenido = Column(Integer, ForeignKey("PeliculasSeries.id_contenido"), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    duracion_vista = Column(Integer)

    # Relaciones
    usuario = relationship("Usuario", back_populates="visualizaciones")
    contenido = relationship("PeliculasSeries", back_populates="visualizaciones_relacion")  # Coincide con el nombre en PeliculasSeries

