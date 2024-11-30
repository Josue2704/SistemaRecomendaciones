from sqlalchemy.orm import Session
from Models.PeliculasSeries import PeliculasSeries
from Models.Comentarios import Comentarios
from sqlalchemy import func


class PeliculasSeriesRepository:
    def __init__(self, db: Session):
        self.db = db

    # Crear contenido
    def crear_contenido(self, contenido: PeliculasSeries):
        try:
            self.db.add(contenido)
            self.db.commit()
            self.db.refresh(contenido)  # Esto asegura que se actualice el `id_contenido` autogenerado
            return contenido  # Retornamos la instancia con todos los campos
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear contenido: {str(e)}")  # Evitamos HTTPException directamente

    # Obtener contenido por ID
    def obtener_contenido_por_id(self, contenido_id: int):
        return self.db.query(PeliculasSeries).filter(PeliculasSeries.id_contenido == contenido_id).first()

    # Listar todo el contenido
    def listar_contenido(self):
        return self.db.query(PeliculasSeries).all()

    # Eliminar contenido
    def eliminar_contenido(self, contenido_id: int):
        contenido = self.obtener_contenido_por_id(contenido_id)
        if contenido:
            self.db.delete(contenido)
            self.db.commit()
        return contenido

    # Obtener todos los contenidos
    def obtener_todos_contenidos(self):
        try:
            return self.db.query(PeliculasSeries).all()
        except Exception as e:
            raise Exception(f"Error al obtener contenidos: {str(e)}")

            # Método para obtener contenido no visto por género

    from sqlalchemy import func

    def obtener_contenido_no_visto_por_genero(self, usuario_id: int, genero: str):
        # Subconsulta para obtener los contenidos que el usuario ya vio
        vistos_subquery = (
            self.db.query(Comentarios.id_contenido)
            .filter(Comentarios.id_usuario == usuario_id)
            .subquery()
        )

        # Consulta para obtener los contenidos del género especificado que no están en la subconsulta
        no_vistos = (
            self.db.query(PeliculasSeries)
            .filter(func.lower(PeliculasSeries.genero) == genero.lower())  # Comparación insensible a mayúsculas
            .filter(PeliculasSeries.id_contenido.notin_(vistos_subquery))  # Excluir contenidos vistos
            .all()
        )
        return no_vistos
