from sqlalchemy.orm import Session
from Models.Visualizaciones import Visualizaciones

class VisualizacionesRepository:
    def __init__(self, db: Session):
        self.db = db

    # Agregar una nueva visualización
    def agregar_visualizacion(self, id_usuario: int, id_contenido: int, duracion_vista: int):
        nueva_visualizacion = Visualizaciones(
            id_usuario=id_usuario,
            id_contenido=id_contenido,
            duracion_vista=duracion_vista
        )
        self.db.add(nueva_visualizacion)
        self.db.commit()
        self.db.refresh(nueva_visualizacion)
        return nueva_visualizacion

    def obtener_historial_por_usuario(self, usuario_id: int):
        # Consulta el historial de visualizaciones con el contenido relacionado
        return (
            self.db.query(Visualizaciones)
            .filter(Visualizaciones.id_usuario == usuario_id)
            .all()
        )
    # Obtener una visualización específica por usuario y contenido
    def obtener_visualizacion(self, id_usuario: int, id_contenido: int):
        return self.db.query(Visualizaciones).filter(
            Visualizaciones.id_usuario == id_usuario,
            Visualizaciones.id_contenido == id_contenido
        ).first()

    # Eliminar una visualización
    def eliminar_visualizacion(self, id_visualizacion: int):
        visualizacion = self.db.query(Visualizaciones).filter(
            Visualizaciones.id_visualizacion == id_visualizacion
        ).first()
        if visualizacion:
            self.db.delete(visualizacion)
            self.db.commit()
        return visualizacion
