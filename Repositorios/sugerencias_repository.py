from sqlalchemy.orm import Session
from Models.Sugerencias import Sugerencias

class SugerenciasRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_sugerencia(self, sugerencia: Sugerencias):
        self.db.add(sugerencia)
        self.db.commit()
        self.db.refresh(sugerencia)
        return sugerencia

    def listar_sugerencias_por_usuario(self, usuario_id: int):
        return self.db.query(Sugerencias).filter(Sugerencias.id_usuario == usuario_id).all()

    def eliminar_sugerencia(self, sugerencia_id: int):
        sugerencia = self.db.query(Sugerencias).filter(Sugerencias.id_sugerencia == sugerencia_id).first()
        if sugerencia:
            self.db.delete(sugerencia)
            self.db.commit()
        return sugerencia


