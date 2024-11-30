from sqlalchemy.orm import Session
from Models.Usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(self, usuario: Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario_por_id(self, usuario_id: int):
        return self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    def listar_usuarios(self):
        return self.db.query(Usuario).all()

    def eliminar_usuario(self, usuario_id: int):
        usuario = self.obtener_usuario_por_id(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
        return usuario
