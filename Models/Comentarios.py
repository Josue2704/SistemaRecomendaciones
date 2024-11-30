from datetime import datetime

from sqlalchemy.orm import relationship

from Connection.database import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON, DECIMAL, Text, Enum, Date, ForeignKey


class Comentarios(Base):
    __tablename__ = "Comentarios"

    id_comentario = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    id_contenido = Column(Integer, ForeignKey("PeliculasSeries.id_contenido"), nullable=False)
    puntaje = Column(DECIMAL(2, 1), nullable=False)
    comentario = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    usuario = relationship("Usuario", back_populates="comentarios")
    contenido = relationship("PeliculasSeries", back_populates="comentarios")

    # Getters and Setters
    def get_puntaje(self):
        return self.puntaje

    def set_puntaje(self, puntaje):
        self.puntaje = puntaje

    def get_comentario(self):
        return self.comentario

    def set_comentario(self, comentario):
        self.comentario = comentario
