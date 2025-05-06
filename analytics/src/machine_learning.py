import tensorflow as tf

def train_model(X_train, y_train):
    # Define el modelo
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])

    # Compila el modelo
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # Entrena el modelo
    model.fit(X_train, y_train, epochs=10)

    return model

# Se implementan los modelos de machine learning, dependiendo de la información
# que se quiera obtener, y de los datos disponibles.
