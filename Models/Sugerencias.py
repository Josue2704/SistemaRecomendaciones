from datetime import datetime

from sqlalchemy.orm import relationship

from Connection.database import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON, DECIMAL, Text, Enum, Date, ForeignKey


class Sugerencias(Base):
    __tablename__ = "Sugerencias"

    id_sugerencia = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    id_contenido = Column(Integer, ForeignKey("PeliculasSeries.id_contenido"), nullable=False)
    razon = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    usuario = relationship("Usuario", back_populates="sugerencias")
    contenido = relationship("PeliculasSeries", back_populates="sugerencias")

    # Getters and Setters
    def get_razon(self):
        return self.razon

    def set_razon(self, razon):
        self.razon = razon

    def get_fecha(self):
        return self.fecha

    def set_fecha(self, fecha):
        self.fecha = fecha
