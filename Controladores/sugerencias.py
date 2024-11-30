from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Connection.database import SessionLocal
from DTOs.SugerenciasDTO import SugerenciasDTO
from Repositorios.sugerencias_repository import SugerenciasRepository
from Models.Sugerencias import Sugerencias

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear una sugerencia
@router.post("/", response_model=SugerenciasDTO)
def crear_sugerencia(sugerencia: SugerenciasDTO, db: Session = Depends(get_db)):
    repo = SugerenciasRepository(db)
    nueva_sugerencia = Sugerencias(**sugerencia.dict())
    return repo.crear_sugerencia(nueva_sugerencia)

# Listar sugerencias de un usuario
@router.get("/usuario/{usuario_id}", response_model=list[SugerenciasDTO])
def listar_sugerencias(usuario_id: int, db: Session = Depends(get_db)):
    repo = SugerenciasRepository(db)
    return repo.listar_sugerencias_por_usuario(usuario_id)
