# alphapp.xyz/content/src/models.py

"""
Define los modelos de datos para el microservicio de gestión de contenidos de Alphapp.
Estos modelos representan la estructura de diferentes tipos de contenido digital,
como artículos, y se utilizan con un ORM (Object-Relational Mapping)
para interactuar con la base de datos.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey # Basado en ejemplos de modelos [1, 2]
from sqlalchemy.orm import relationship # Basado en ejemplos de modelos [2]
from sqlalchemy.ext.declarative import declarative_base # Basado en ejemplos de modelos [1, 2]
import datetime # Necesario para tipos DateTime [2]

# Se utiliza declarative_base() para definir la base para los modelos declarativos [1, 2]
Base = declarative_base()

# Ejemplo de modelo para representar un artículo [3]
# Este modelo sigue el esquema de datos descrito para un artículo [3]
class Article(Base):
    """
    Representa un artículo de contenido digital.
    Corresponde a un tipo de contenido gestionado por el CMS modular [4, 5].
    """
    __tablename__ = 'articles' # Define el nombre de la tabla en la base de datos [1, 2]

    # Campos del modelo basados en el esquema de ejemplo [3] y tipos comunes [1, 2]
    id = Column(Integer, primary_key=True) # Identificador único del artículo [3]
    title = Column(String(255), nullable=False) # Título del artículo [3]
    content = Column(Text, nullable=False) # Contenido principal del artículo (usando Text para contenido largo) [2, 3]
    author_id = Column(Integer, ForeignKey('users.id')) # Identificador del autor (ForeignKey a la tabla de usuarios, asumiendo que existe una tabla 'users' en el servicio de usuarios) [2, 3]
    publication_date = Column(DateTime, default=datetime.datetime.utcnow) # Fecha de publicación (usando DateTime) [2, 3]
    # Los tags podrían gestionarse a través de una tabla de relación muchos a muchos,
    # pero para simplificar, se omite aquí o se podría usar un tipo de dato de array si la DB lo soporta.
    # tags = Column(ARRAY(String)) # Ejemplo conceptual para tags, si la DB soporta arrays

    # Relación con el autor (asumiendo un modelo User en otro microservicio/contexto o en la misma DB si la arquitectura lo permite) [2, 3]
    # author = relationship('User') # Esta línea requeriría que el modelo User esté definido o importado

    def __repr__(self):
        """
        Representación del objeto Article para depuración.
        """
        return f"<Article(id={self.id}, title='{self.title}', author_id={self.author_id})>"

# Otros modelos para diferentes tipos de contenido (videos, imágenes, documentos, etc.)
# se definirían de manera similar, cada uno con su propio esquema de datos [3, 4].

# class Video(Base):
#     __tablename__ = 'videos'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False)
#     url = Column(String(512), nullable=False)
#     # ... otros campos específicos de video

# Los modelos de relación entre contenidos (por ejemplo, Artículo con Comentarios)
# se definirían aquí si los comentarios forman parte de este microservicio,
# o en el microservicio de comunidad si allí se gestionan los comentarios [6].

# class Comment(Base):
#     __tablename__ = 'comments'
#     id = Column(Integer, primary_key=True)
#     content = Column(Text, nullable=False)
#     article_id = Column(Integer, ForeignKey('articles.id'))
#     author_id = Column(Integer, ForeignKey('users.id'))
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     # article = relationship('Article', backref='comments')
#     # author = relationship('User')
