from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Connection.database import SessionLocal
from Models.PeliculasSeries import PeliculasSeries
from Repositorios.usuarios_repository import UsuarioRepository
from Repositorios.peliculas_series_repository import PeliculasSeriesRepository
import tensorflow as tf
import numpy as np  # Asegura el manejo correcto de los datos para TensorFlow

# Crear el router
router = APIRouter()

# Cargar el modelo entrenado
modelo_recomendacion = tf.keras.models.load_model("modelo_recomendacion.keras")

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{usuario_id}/genero/{genero}")
def generar_recomendaciones_por_genero(usuario_id: int, genero: str, db: Session = Depends(get_db)):
    repo_usuario = UsuarioRepository(db)
    repo_contenido = PeliculasSeriesRepository(db)

    usuario = repo_usuario.obtener_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    contenidos = repo_contenido.obtener_contenido_no_visto_por_genero(usuario_id, genero)
    if not contenidos:
        raise HTTPException(status_code=404, detail="No hay contenido disponible para este género")

    recomendaciones = []
    for contenido in contenidos:
        try:
            prediccion = modelo_recomendacion.predict([
                np.array([usuario.id_usuario]),
                np.array([contenido.id_contenido])
            ])
            recomendaciones.append({
                "titulo": contenido.nombre,
                "puntaje": float(prediccion[0][0])
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al generar la predicción: {str(e)}")

    recomendaciones = sorted(recomendaciones, key=lambda x: x["puntaje"], reverse=True)
    return {"usuario": usuario.nombre, "genero": genero, "recomendaciones": recomendaciones[:10]}

# Suponiendo que obtuviste los valores máximos de input_dim
MAX_USUARIOS = 8  # Cambiar según el modelo
MAX_CONTENIDOS = 8 # Cambiar según el modelo

@router.get("/{usuario_id}")
def generar_recomendaciones(usuario_id: int, db: Session = Depends(get_db)):
    repo_usuario = UsuarioRepository(db)
    repo_contenido = PeliculasSeriesRepository(db)

    # Verificar que el usuario existe
    usuario = repo_usuario.obtener_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener todos los contenidos
    contenidos = repo_contenido.obtener_todos_contenidos()
    if not contenidos:
        raise HTTPException(status_code=404, detail="No hay contenido disponible para recomendar")

    recomendaciones = []
    for contenido in contenidos:
        usuario_input = np.array([usuario.id_usuario])
        contenido_input = np.array([contenido.id_contenido])

        # Validar rangos de IDs
        if usuario_input[0] >= MAX_USUARIOS or contenido_input[0] >= MAX_CONTENIDOS:
            continue  # Ignorar IDs fuera del rango permitido

        # Generar predicción
        try:
            prediccion = modelo_recomendacion.predict([usuario_input, contenido_input])
            recomendaciones.append({
                "titulo": contenido.nombre,
                "puntaje": float(prediccion[0][0])
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al generar la predicción: {str(e)}")

    recomendaciones = sorted(recomendaciones, key=lambda x: x["puntaje"], reverse=True)
    return {"usuario": usuario.nombre, "recomendaciones": recomendaciones[:10]}
