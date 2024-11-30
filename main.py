from fastapi import FastAPI
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


# Cargar el modelo entrenado
modelo_recomendacion = tf.keras.models.load_model("modelo_recomendacion.keras")

# Crear la aplicación FastAPI
app = FastAPI()

# Agregar controladores
from Controladores import usuarios, peliculas_series, comentarios, sugerencias, recomendaciones
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(peliculas_series.router, prefix="/peliculas-series", tags=["PeliculasSeries"])
app.include_router(comentarios.router, prefix="/comentarios", tags=["Comentarios"])
app.include_router(sugerencias.router, prefix="/sugerencias", tags=["Sugerencias"])
app.include_router(recomendaciones.router, prefix="/recomendaciones", tags=["Recomendaciones"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)