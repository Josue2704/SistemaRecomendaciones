import tensorflow as tf
import numpy as np
import pymysql
import pandas as pd

# Conexión a la base de datos MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',  # Cambia a tu usuario de MySQL
    password='',  # Deja vacío si no tienes contraseña
    database='SistemaRecomendacion'
)

# Extraer datos de interacciones (visualizaciones y calificaciones)
query = """
SELECT
    v.id_usuario,
    v.id_contenido,
    IFNULL(c.puntaje, 3.0) AS puntaje -- Usar puntaje 3.0 como predeterminado si no hay comentarios
FROM Visualizaciones v
LEFT JOIN Comentarios c ON v.id_usuario = c.id_usuario AND v.id_contenido = c.id_contenido
"""
df_interacciones = pd.read_sql(query, connection)

# Cerrar la conexión a la base de datos
connection.close()

# Verificar datos cargados
print("Datos de interacciones cargados:")
print(df_interacciones.head())

# Convertir los datos en tensores
usuarios = df_interacciones['id_usuario'].values
contenidos = df_interacciones['id_contenido'].values
calificaciones = df_interacciones['puntaje'].values

usuarios_tensor = tf.constant(usuarios, dtype=tf.int32)
contenidos_tensor = tf.constant(contenidos, dtype=tf.int32)
calificaciones_tensor = tf.constant(calificaciones, dtype=tf.float32)

# Definir dimensiones para embeddings
num_usuarios = usuarios_tensor.numpy().max() + 1
num_contenidos = contenidos_tensor.numpy().max() + 1
embedding_dim = 8  # Dimensión del espacio latente

# Crear embeddings para usuarios y contenidos
usuario_embedding = tf.keras.layers.Embedding(input_dim=num_usuarios, output_dim=embedding_dim)
contenido_embedding = tf.keras.layers.Embedding(input_dim=num_contenidos, output_dim=embedding_dim)

# Construir el modelo
usuario_input = tf.keras.layers.Input(shape=(), dtype=tf.int32, name='usuario_id')
contenido_input = tf.keras.layers.Input(shape=(), dtype=tf.int32, name='contenido_id')

usuario_vec = usuario_embedding(usuario_input)
contenido_vec = contenido_embedding(contenido_input)

dot_product = tf.keras.layers.Dot(axes=1)([usuario_vec, contenido_vec])  # Producto punto
output = tf.keras.layers.Activation('sigmoid')(dot_product)  # Activación sigmoid para normalizar

model = tf.keras.Model(inputs=[usuario_input, contenido_input], outputs=output)

# Compilar el modelo
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenar el modelo
print("Entrenando el modelo...")
model.fit(
    x=[usuarios_tensor, contenidos_tensor],
    y=calificaciones_tensor,
    batch_size=16,
    epochs=10
)

# Guardar el modelo en formato Keras recomendado
model.save("modelo_recomendacion.keras")
print("Modelo guardado en 'modelo_recomendacion.keras'")

