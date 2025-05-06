# alphapp.xyz/content/src/views.py

"""
Define las vistas (endpoints de la API) para el microservicio de gestión de contenidos de Alphapp.
Maneja las solicitudes HTTP entrantes, interactúa con la lógica de negocio/modelos
y utiliza serializadores para formatear las respuestas en JSON.
"""

# Importar el framework web (ej. Flask o FastAPI). Usaremos Flask para este ejemplo conceptual.
# En un proyecto real, la elección dependería de la infraestructura específica.
from flask import Flask, jsonify, request, abort
import json # Importar json para simular la entrada/salida
import datetime # Necesario para manejar fechas como en el esquema JSON
# Importar el serializador definido en serializers.py
# from .serializers import ArticleSerializer # Ejemplo de importación real

# Simulación conceptual del serializador para el ejemplo
class ConceptualArticleSerializer:
    def serialize(self, article):
        """Simula la serialización de un objeto artículo a diccionario."""
        # Mapea al esquema JSON del artículo [10]
        return {
            "id": article.get("id"),
            "title": article.get("title"),
            "content": article.get("content"), # Usamos 'content' como en el esquema [10]
            "author": article.get("author"), # Mapea a 'author' como en el esquema [10]
            "publication_date": article.get("publication_date").isoformat() if article.get("publication_date") else None,
            "tags": article.get("tags", [])
        }
    def serialize_many(self, articles):
        """Simula la serialización de una lista de artículos."""
        return [self.serialize(article) for article in articles]
    # Deserialización conceptual (usada para POST/PUT)
    def deserialize(self, data: dict) -> dict:
         """Simula la deserialización de datos de entrada a formato utilizable."""
         # Validación básica y mapeo a formato interno (podría ser diferente del modelo directo)
         deserialized_data = {
             "title": data.get("title"),
             "content": data.get("content"),
             "tags": data.get("tags", []),
             # Aquí podrías obtener el author_id del token JWT validado por el API Gateway
             "author_id": data.get("author_id", 1) # Simulado: Asignar un author_id por defecto o del contexto
         }
         # Validación de campos obligatorios (ejemplo conceptual)
         if not deserialized_data.get("title") or not deserialized_data.get("content"):
              # En un caso real, se levantaría una excepción de validación
             print("Validación fallida: Faltan título o contenido")
             return None # Indicar fallo
         return deserialized_data


# Importar los modelos (simulados para el ejemplo)
# from .models import Article # Ejemplo de importación real
# Simulación conceptual de interacción con la base de datos/modelos
class ConceptualContentRepository:
    """Simula la interacción con la capa de datos."""
    def __init__(self):
        # Simulación de una base de datos en memoria
        self._articles = [
            {"id": 1, "title": "Artículo de Prueba 1", "content": "Contenido del artículo 1.", "author_id": 101, "author": "Autor Ejemplo 1", "publication_date": datetime.datetime.utcnow() - datetime.timedelta(days=5), "tags": ["tecnología", "ejemplo"]},
            {"id": 2, "title": "Artículo de Prueba 2", "content": "Contenido del artículo 2.", "author_id": 102, "author": "Autor Ejemplo 2", "publication_date": datetime.datetime.utcnow() - datetime.timedelta(days=2), "tags": ["programación", "ejemplo"]}
        ]
        self._next_id = 3

    def get_all_articles(self):
        # En un caso real, aplicar paginación, filtrado, búsqueda [17, 18]
        return self._articles

    def get_article_by_id(self, article_id):
        for article in self._articles:
            if article["id"] == article_id:
                return article
        return None # No encontrado

    def create_article(self, article_data):
        # article_data vendría deserializado de la entrada [10]
        new_article = {
            "id": self._next_id,
            "title": article_data["title"],
            "content": article_data["content"],
            "author_id": article_data.get("author_id", 1), # Usar author_id del data o un valor por defecto
            "author": f"Autor ID {article_data.get('author_id', 1)}", # Simulado: Generar nombre de autor
            "publication_date": datetime.datetime.utcnow(), # Fecha actual al crear
            "tags": article_data.get("tags", [])
        }
        self._articles.append(new_article)
        self._next_id += 1
        return new_article

    def update_article(self, article_id, update_data):
        # update_data vendría deserializado de la entrada
        for article in self._articles:
            if article["id"] == article_id:
                # Actualizar solo los campos presentes en update_data
                if "title" in update_data:
                    article["title"] = update_data["title"]
                if "content" in update_data:
                    article["content"] = update_data["content"]
                if "tags" in update_data:
                     article["tags"] = update_data["tags"]
                # Otros campos como author_id o publication_date podrían no ser actualizables vía API
                return article
        return None # No encontrado

    def delete_article(self, article_id):
        initial_count = len(self._articles)
        self._articles = [article for article in self._articles if article["id"] != article_id]
        return len(self._articles) < initial_count # True si se eliminó algo

app = Flask(__name__)
article_serializer = ConceptualArticleSerializer()
content_repository = ConceptualContentRepository() # Instancia del repositorio simulado

# Endpoint para obtener todos los artículos o crear uno nuevo [13, 14]
@app.route('/articles', methods=['GET', 'POST'])
def articles_list_create():
    # En un entorno real, la autenticación/autorización se verifica aquí o en el API Gateway [5, 9, 15, 16]
    # Por ejemplo: if not is_authenticated(): return jsonify({"message": "No autorizado"}), 401

    if request.method == 'GET':
        # Lógica para manejar parámetros de paginación, filtrado, búsqueda [17, 18]
        # page = request.args.get('page', 1, type=int)
        # limit = request.args.get('limit', 10, type=int)
        # filter_tag = request.args.get('tags')
        # search_query = request.args.get('search')

        # Obtener artículos de la capa de datos (repositorio/modelo)
        # Aplicar lógica de paginación/filtrado/búsqueda si los parámetros existen
        all_articles = content_repository.get_all_articles() # Simplicidad, sin paginación/filtrado real aquí

        # Serializar la lista de objetos a diccionarios JSON [1, 4, 5]
        serialized_articles = article_serializer.serialize_many(all_articles)

        # Devolver la respuesta JSON con código 200 OK
        # En un caso real, añadir metadatos de paginación si aplica [17]
        return jsonify(serialized_articles), 200

    elif request.method == 'POST':
        # Crear un nuevo artículo
        data = request.get_json() # Obtener datos JSON del cuerpo de la solicitud

        # Deserializar y validar los datos entrantes [1, 4]
        deserialized_data = article_serializer.deserialize(data)

        # Verificar si la deserialización/validación fue exitosa
        if deserialized_data is None:
             return jsonify({"message": "Datos de entrada no válidos"}), 400 # Bad Request [19]

        # En un caso real, el author_id se obtendría del contexto de autenticación
        # deserialized_data['author_id'] = get_user_id_from_auth_context()

        # Crear el artículo usando la capa de datos (repositorio/modelo)
        try:
            new_article = content_repository.create_article(deserialized_data)
        except Exception as e:
            # Manejo de errores, ej. error de base de datos
            print(f"Error al crear artículo: {e}")
            return jsonify({"message": "Error interno al crear artículo"}), 500 # Internal Server Error

        # Serializar el nuevo objeto creado para la respuesta [1, 4, 5]
        serialized_new_article = article_serializer.serialize(new_article)

        # Devolver la respuesta JSON con código 201 Created [20]
        return jsonify(serialized_new_article), 201

# Endpoint para obtener, actualizar o eliminar un artículo específico por ID [13, 14]
@app.route('/articles/<int:article_id>', methods=['GET', 'PUT', 'DELETE'])
def article_detail(article_id):
    # En un entorno real, la autenticación/autorización y verificación de permisos se realizaría aquí [5, 9, 15, 16]
    # Por ejemplo: if not can_access_article(user, article_id): return jsonify({"message": "Prohibido"}), 403

    # Obtener el artículo de la capa de datos
    article = content_repository.get_article_by_id(article_id)

    # Si el artículo no se encuentra, devolver 404 Not Found [19]
    if article is None:
        abort(404) # Flask Abort generará una respuesta 404 estándar

    if request.method == 'GET':
        # Serializar el objeto Article a un diccionario JSON [1, 4, 5]
        serialized_article = article_serializer.serialize(article)

        # Devolver la respuesta JSON con código 200 OK
        return jsonify(serialized_article), 200

    elif request.method == 'PUT':
        # Actualizar el artículo existente
        data = request.get_json() # Obtener datos JSON del cuerpo de la solicitud

        # Deserializar y validar los datos entrantes (solo campos permitidos para actualizar)
        # Podrías tener un serializador de actualización diferente
        deserialized_update_data = {}
        if 'title' in data:
            deserialized_update_data['title'] = data['title']
        if 'content' in data:
            deserialized_update_data['content'] = data['content']
        if 'tags' in data:
             deserialized_update_data['tags'] = data['tags']

        if not deserialized_update_data: # Si no hay campos válidos para actualizar
             return jsonify({"message": "No hay campos válidos para actualizar"}), 400

        # En un caso real, verificar que el usuario autenticado sea el autor del artículo para actualizar

        # Actualizar el artículo usando la capa de datos (repositorio/modelo)
        try:
            updated_article = content_repository.update_article(article_id, deserialized_update_data)
        except Exception as e:
             print(f"Error al actualizar artículo: {e}")
             return jsonify({"message": "Error interno al actualizar artículo"}), 500

        # Serializar el objeto actualizado para la respuesta [1, 4, 5]
        serialized_updated_article = article_serializer.serialize(updated_article)

        # Devolver la respuesta JSON con código 200 OK
        return jsonify(serialized_updated_article), 200

    elif request.method == 'DELETE':
        # Eliminar el artículo
        # En un caso real, verificar que el usuario autenticado tenga permisos para eliminar

        # Eliminar el artículo usando la capa de datos (repositorio/modelo)
        try:
            is_deleted = content_repository.delete_article(article_id)
            if not is_deleted: # Esto no debería ocurrir si article se encontró arriba, pero es buena práctica
                 abort(404)
        except Exception as e:
             print(f"Error al eliminar artículo: {e}")
             return jsonify({"message": "Error interno al eliminar artículo"}), 500

        # Devolver una respuesta exitosa (código 200 OK o 204 No Content) [14] muestra 200 con mensaje
        return jsonify({"message": f"Artículo con ID {article_id} eliminado"}), 200 # O return '', 204

# --- Ejemplo de cómo ejecutar la aplicación (para desarrollo/testing local) ---
if __name__ == '__main__':
    # Cuando se ejecuta este archivo directamente, se inicia el servidor Flask
    # En producción, se usaría un servidor WSGI como Gunicorn o uWSGI
    # app.run(debug=True) # Habilitar debug para desarrollo
     print("Corriendo el microservicio de contenido (simulado)")
     print("Ejemplo: GET /articles")
     print("Ejemplo: POST /articles con body: {'title': 'Test', 'content': 'Contenido', 'tags': ['a'] }")
     print("Ejemplo: GET /articles/1")
     print("Ejemplo: PUT /articles/1 con body: {'content': 'Contenido Actualizado'}")
     print("Ejemplo: DELETE /articles/1")

     # Simular una solicitud GET para demostrar
     # from flask.testing import FlaskClient
     # with app.test_client() as c:
     #     rv = c.get('/articles')
     #     print("\nRespuesta GET /articles:")
     #     print(rv.data.decode('utf-8'))

     # Nota: Para probar POST/PUT/DELETE necesitarías herramientas como curl o Postman

