from sqlalchemy.orm import Session
from Models.Comentarios import Comentarios

class ComentariosRepository:
    def __init__(self, db: Session):
        self.db = db

    def agregar_comentario(self, comentario: Comentarios):
        self.db.add(comentario)
        self.db.commit()
        self.db.refresh(comentario)
        return comentario

    def listar_comentarios_por_contenido(self, contenido_id: int):
        try:
            return self.db.query(Comentarios).filter(Comentarios.id_contenido == contenido_id).all()
        except Exception as e:
            raise Exception(f"Error al listar comentarios: {str(e)}")

    def eliminar_comentario(self, comentario_id: int):
        comentario = self.db.query(Comentarios).filter(Comentarios.id_comentario == comentario_id).first()
        if comentario:
            self.db.delete(comentario)
            self.db.commit()
        return comentario
