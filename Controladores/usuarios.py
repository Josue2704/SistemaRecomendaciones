from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Connection.database import SessionLocal
from DTOs import UsuarioCreateDTO, UsuarioResponseDTO
from sqlalchemy.exc import IntegrityError
from Repositorios.usuarios_repository import UsuarioRepository
from Models.Usuario import Usuario  # Modificado
from Repositorios.visualizaciones_repository import VisualizacionesRepository

router = APIRouter()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{usuario_id}/historial")
def obtener_historial_visualizaciones(usuario_id: int, db: Session = Depends(get_db)):
    repo_visualizaciones = VisualizacionesRepository(db)

    historial = repo_visualizaciones.obtener_historial_por_usuario(usuario_id)
    if not historial:
        raise HTTPException(status_code=404, detail="No hay historial para este usuario")

    return {"usuario_id": usuario_id, "historial": historial}


# Crear un usuario
@router.post("/", response_model=UsuarioResponseDTO)
def crear_usuario(usuario: UsuarioCreateDTO, db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        edad=usuario.edad,
        nacionalidad=usuario.nacionalidad,
        preferencias=usuario.preferencias,
        ubicacion=usuario.ubicacion,
        email=usuario.email,
        contraseña_hash="hashed_" + usuario.contraseña  # Hash real en producción
    )
    try:
        return repo.crear_usuario(nuevo_usuario)
    except IntegrityError as e:
        db.rollback()  # Revertir cualquier cambio en la base de datos
        if "email" in str(e.orig):  # Verificar si el error se relaciona con el email
            raise HTTPException(
                status_code=400, detail="El correo electrónico ya está registrado."
            )
        raise HTTPException(
            status_code=500, detail="Error al crear el usuario."
        )
# Obtener todos los usuarios
@router.get("/", response_model=list[UsuarioResponseDTO])
def listar_usuarios(db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    return repo.listar_usuarios()

# Obtener un usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioResponseDTO)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    usuario = repo.obtener_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Eliminar un usuario
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    usuario = repo.eliminar_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}

