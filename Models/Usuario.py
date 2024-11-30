from datetime import datetime

from sqlalchemy.orm import relationship

from Connection.database import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON

class Usuario(Base):
    __tablename__ = "Usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer)
    nacionalidad = Column(String(50))
    preferencias = Column(JSON)
    ubicacion = Column(String(255))
    email = Column(String(100), unique=True, nullable=False)
    contraseña_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relación con Comentarios y Sugerencias
    comentarios = relationship("Comentarios", back_populates="usuario")
    sugerencias = relationship("Sugerencias", back_populates="usuario")
    # Relación con Visualizaciones
    visualizaciones = relationship("Visualizaciones", back_populates="usuario")

    # Getters and Setters
    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_contraseña(self):
        return self.contraseña_hash

    def set_contraseña(self, contraseña):
        self.contraseña_hash = contraseña
