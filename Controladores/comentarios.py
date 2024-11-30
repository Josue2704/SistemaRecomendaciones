from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Connection.database import SessionLocal
from DTOs.ComentariosDTO import ComentariosDTO
from Repositorios.comentarios_repository import ComentariosRepository
from Models.Comentarios import Comentarios

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Agregar un comentario
@router.post("/", response_model=ComentariosDTO)
def agregar_comentario(comentario: ComentariosDTO, db: Session = Depends(get_db)):
    repo = ComentariosRepository(db)
    nuevo_comentario = Comentarios(**comentario.dict())
    return repo.agregar_comentario(nuevo_comentario)

# Listar comentarios de un contenido
@router.get("/contenido/{contenido_id}", response_model=list[ComentariosDTO])
def listar_comentarios(contenido_id: int, db: Session = Depends(get_db)):
    repo = ComentariosRepository(db)
    try:
        comentarios = repo.listar_comentarios_por_contenido(contenido_id)
        if not comentarios:
            raise HTTPException(status_code=404, detail="No hay comentarios para este contenido.")
        return comentarios
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
