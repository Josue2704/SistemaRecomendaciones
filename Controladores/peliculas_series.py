from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Connection.database import SessionLocal
from DTOs.PeliculasDTO import PeliculasSeriesResponseDTO
from DTOs.PeliculasDTO import PeliculasSeriesCreateDTO
from Repositorios.peliculas_series_repository import PeliculasSeriesRepository
from Models.PeliculasSeries import PeliculasSeries

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear contenido
# Crear contenido
@router.post("/", response_model=PeliculasSeriesResponseDTO)
def crear_contenido(contenido: PeliculasSeriesCreateDTO, db: Session = Depends(get_db)):
    try:
        repo = PeliculasSeriesRepository(db)
        nuevo_contenido = PeliculasSeries(**contenido.dict())
        return repo.crear_contenido(nuevo_contenido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear contenido: {str(e)}")

# Listar contenido
@router.get("/", response_model=list[PeliculasSeriesResponseDTO])
def listar_contenidos(db: Session = Depends(get_db)):
    repo = PeliculasSeriesRepository(db)
    return repo.listar_contenido()
# Obtener contenido por ID
@router.get("/{contenido_id}", response_model=PeliculasSeriesResponseDTO)
def obtener_contenido(contenido_id: int, db: Session = Depends(get_db)):
    repo = PeliculasSeriesRepository(db)
    contenido = repo.obtener_contenido_por_id(contenido_id)
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return contenido
