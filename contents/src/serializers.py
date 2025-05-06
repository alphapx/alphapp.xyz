# alphapp.xyz/content/src/serializers.py

"""
Define los serializadores para el microservicio de gestión de contenidos de Alphapp.
Estos serializadores se encargan de transformar los objetos del modelo de datos
(como Article) a formatos adecuados para las respuestas de la API (principalmente JSON)
y, opcionalmente, de deserializar los datos de entrada de la API a formatos utilizables
por la lógica de negocio.
"""

# Importar los modelos necesarios desde models.py
# Aunque models.py ya define el modelo Article, aquí lo conceptualizamos
# para demostrar cómo el serializador interactúa con él.
# En un proyecto real, importarías la clase Article.
# from .models import Article # Ejemplo de importación real

# Simulación conceptual de una clase Article para el ejemplo del serializador
# En un proyecto real, esta clase vendría del archivo models.py
class ConceptualArticleModel:
    """Representación conceptual del modelo Article para propósitos de serialización."""
    def __init__(self, id, title, content, author_id, publication_date, tags=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.publication_date = publication_date
        self.tags = tags if tags is not None else []

# Serializador para el modelo Article
class ArticleSerializer:
    """
    Serializador para el modelo Article.
    Transforma objetos Article a diccionarios (que pueden ser convertidos a JSON)
    y viceversa (deserialización, opcional).
    """

    def serialize(self, article: ConceptualArticleModel) -> dict:
        """
        Serializa un objeto Article a un diccionario.
        El diccionario resultante sigue el esquema JSON definido para artículos [8].
        """
        # Transforma el objeto Article a un diccionario Python
        # que mapea a la estructura JSON esperada por la API [8].
        serialized_data = {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            # Nota: El esquema JSON [8] tiene "author", aquí mapeamos author_id
            # Asumimos que la API Gateway o la vista manejaría la expansión si es necesaria.
            # O, si el modelo Article tuviera una relación cargada, se serializaría el objeto author.
            "author_id": article.author_id, # Usamos author_id del modelo conceptual
            "publication_date": article.publication_date.isoformat() if article.publication_date else None, # Convertir DateTime a string ISO 8601
            "tags": article.tags # Los tags son una lista en el esquema [8]
        }
        return serialized_data

    def serialize_many(self, articles: list[ConceptualArticleModel]) -> list[dict]:
        """
        Serializa una lista de objetos Article a una lista de diccionarios.
        """
        return [self.serialize(article) for article in articles]

    # Opcionalmente, se puede incluir lógica para deserializar datos entrantes (por ejemplo, JSON)
    # a un formato que la lógica de negocio pueda usar para crear/actualizar modelos.
    # Las vistas de la API (views.py) a menudo utilizan esta funcionalidad [9, 10].
    # def deserialize(self, data: dict) -> dict:
    #     """
    #     Deserializa un diccionario (por ejemplo, de JSON entrante) a un formato
    #     utilizable para crear o actualizar un objeto Article.
    #     """
    #     # Aquí se realizaría validación y transformación inversa si es necesario.
    #     # Este es un ejemplo simplificado.
    #     deserialized_data = {
    #         "title": data.get("title"),
    #         "content": data.get("content"),
    #         # author_id podría venir de la autenticación o del cuerpo, dependiendo del diseño
    #         "author_id": data.get("author_id"),
    #         "tags": data.get("tags", [])
    #         # publication_date podría establecerse automáticamente o venir en la solicitud
    #     }
    #     # Se podría añadir validación más robusta aquí
    #     if not deserialized_data["title"] or not deserialized_data["content"]:
    #          # Levantar una excepción o devolver un error
    #          pass # Ejemplo conceptual
    #     return deserialized_data

# --- Ejemplo de uso (solo para demostración, no parte del archivo real) ---
if __name__ == "__main__":
    import datetime
    # Simular un objeto Article obtenido de la base de datos
    articulo_ejemplo = ConceptualArticleModel(
        id=1,
        title="Mi Primer Artículo",
        content="Este es el contenido de mi primer artículo.",
        author_id=101,
        publication_date=datetime.datetime.utcnow(),
        tags=["prueba", "ejemplo", "contenido"]
    )

    # Crear una instancia del serializador
    serializer = ArticleSerializer()

    # Serializar el objeto Article a un diccionario
    articulo_serializado = serializer.serialize(articulo_ejemplo)

    import json
    # Imprimir el JSON resultante (ejemplo)
    print("Artículo Serializado (Diccionario/JSON):")
    print(json.dumps(articulo_serializado, indent=4))

    # Simular una lista de artículos
    articulo_ejemplo_2 = ConceptualArticleModel(
        id=2,
        title="Segundo Artículo",
        content="Más contenido de prueba.",
        author_id=102,
        publication_date=datetime.datetime.utcnow(),
        tags=["segundo", "prueba"]
    )
    lista_articulos_ejemplo = [articulo_ejemplo, articulo_ejemplo_2]

    # Serializar la lista de artículos
    lista_serializada = serializer.serialize_many(lista_articulos_ejemplo)

    print("\nLista de Artículos Serializados (Lista de Diccionarios/JSON):")
    print(json.dumps(lista_serializada, indent=4))

    # --- Ejemplo conceptual de deserialización (si la lógica estuviera implementada) ---
    # data_recibida_api = {
    #     "title": "Nuevo Artículo desde API",
    #     "content": "Contenido enviado vía API.",
    #     "tags": ["api", "nuevo"]
    #     # author_id se podría obtener del token JWT [3, 11, 12]
    # }
    # print("\nEjemplo conceptual de Deserialización:")
    # deserialized_data = serializer.deserialize(data_recibida_api)
    # print(deserialized_data)
