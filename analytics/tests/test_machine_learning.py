import pytest
import numpy as np
import tensorflow as tf

# Importar las funciones del archivo machine_learning.py para probar
# Suponiendo que el archivo a probar está en la misma estructura de proyecto
# en la carpeta 'src'
from src.machine_learning import train_model # Importar la función train_model mostrada en las fuentes

# fixture para crear datos de ejemplo para las pruebas de ML
@pytest.fixture
def sample_training_data():
    """
    Fixture para crear datos de entrenamiento de ejemplo (NumPy arrays).
    Simula datos simples para un problema de clasificación binaria.
    """
    X_train = np.random.rand(100, 10).astype(np.float32) # 100 muestras, 10 características
    y_train = np.random.randint(0, 2, 100).astype(np.int32) # Etiquetas binarias (0 o 1)
    return X_train, y_train

def test_train_model_returns_keras_model(sample_training_data):
    """
    Prueba que la función train_model retorna un objeto de modelo Keras.
    """
    X_train, y_train = sample_training_data

    # Entrenar el modelo con los datos de ejemplo
    model = train_model(X_train, y_train)

    # Verificar que el objeto retornado es una instancia de un modelo Keras
    assert isinstance(model, tf.keras.models.Model)

def test_train_model_produces_a_trained_model(sample_training_data):
    """
    Prueba básica para verificar que el modelo retornado se puede usar para predecir.
    (No verifica la precisión del entrenamiento, solo la funcionalidad básica).
    """
    X_train, y_train = sample_training_data

    # Entrenar el modelo
    model = train_model(X_train, y_train)

    # Crear datos de ejemplo para predicción (una sola muestra)
    X_predict = np.random.rand(1, 10).astype(np.float32)

    # Intentar realizar una predicción
    try:
        predictions = model.predict(X_predict)
        # Verificar que la predicción retorna algo (ej. un array de NumPy)
        assert isinstance(predictions, np.ndarray)
        # Verificar que la forma de la salida es la esperada (ej. 1 muestra, 10 clases de salida del ejemplo original)
        assert predictions.shape == (1, 10) # Basado en el ejemplo tf.keras.layers.Dense(10) en src/machine_learning.py
    except Exception as e:
        pytest.fail(f"La predicción falló después del entrenamiento: {e}")


# Se realizan pruebas unitarias para los modelos de aprendizaje automático.
# Se utiliza pytest para ejecutar las pruebas.
# Se utilizan assertions para verificar que las funciones retornan objetos correctos y son utilizables.
# Este es un ejemplo básico; las pruebas de ML en un entorno real serían más complejas.
