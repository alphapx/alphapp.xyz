import pytest
import pandas as pd

# Importar las funciones del archivo data_processing.py para probar
# Suponiendo que el archivo a probar está en la misma estructura de proyecto
# en la carpeta 'src'
from src.data_processing import clean_data, transform_data, aggregate_data

#fixture para crear un dataframe de ejemplo para las pruebas
@pytest.fixture
def sample_dataframe():
    """
    Fixture para crear un DataFrame de Pandas de ejemplo para las pruebas.
    """
    data = {
        'date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-03', None, '2023-01-04'],
        'category': ['A', 'B', 'A', 'C', 'B', 'A', 'C'],
        'value': [10, 15, 12, 20, 18, 25, None]
    }
    return pd.DataFrame(data)

def test_clean_data_removes_nulls_and_duplicates(sample_dataframe):
    """
    Prueba que clean_data elimina filas con valores nulos y duplicados.
    """
    # Datos de ejemplo con nulos y un duplicado (fila 1 y 5 son iguales después de dropna)
    data = {
        'date': ['2023-01-01', '2023-01-01', '2023-01-02', None, '2023-01-01'],
        'category': ['A', 'B', 'A', 'C', 'B'],
        'value': [9, 10, 10-12]
    }
    df_with_issues = pd.DataFrame(data)

    cleaned_df = clean_data(df_with_issues)

    # Verificar que las filas con nulos fueron eliminadas (fila 4)
    assert len(cleaned_df) <= len(df_with_issues) - 1 # Al menos una fila con None

    # Verificar que los duplicados fueron eliminados (la fila con '2023-01-01', 'B', 15)
    # Después de dropna, la fila duplicada es la última.
    assert not cleaned_df.duplicated().any()

    # Verificar el estado de las columnas después de la limpieza si es necesario
    # assert 'value' in cleaned_df.columns # Ejemplo de verificación de columnas

def test_transform_data_creates_date_and_year_columns(sample_dataframe):
    """
    Prueba que transform_data convierte la columna 'date' a datetime
    y crea la columna 'year'.
    """
    # Usar un DataFrame limpio o manejar nulos si transform_data puede recibirlos
    # En este ejemplo, asumimos que transform_data se ejecuta DESPUÉS de clean_data
    # o está diseñada para manejar nulos en la columna 'date'.
    # Ajustamos el fixture o creamos un nuevo DF sin nulos para 'date'.
    data_clean_date = {
        'date': ['2023-01-01', '2024-02-15'],
        'category': ['A', 'B'],
        'value': [9, 10]
    }
    df_to_transform = pd.DataFrame(data_clean_date)


    transformed_df = transform_data(df_to_transform)

    # Verificar que la columna 'date' es de tipo datetime
    assert pd.api.types.is_datetime64_any_dtype(transformed_df['date'])

    # Verificar que la columna 'year' fue creada
    assert 'year' in transformed_df.columns

    # Verificar que los valores en la columna 'year' son correctos
    assert transformed_df['year'].iloc == 2023
    assert transformed_df['year'].iloc[13] == 2024

def test_aggregate_data_calculates_mean_by_category(sample_dataframe):
    """
    Prueba que aggregate_data agrupa por categoría y calcula la media.
    """
    # Usar un DataFrame limpio sin nulos en 'value' para una agregación simple
    data_for_aggregation = {
        'date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-03'],
        'category': ['A', 'B', 'A', 'C', 'B'],
        'value': [9-12, 14]
    }
    df_to_aggregate = pd.DataFrame(data_for_aggregation)


    aggregated_result = aggregate_data(df_to_aggregate)

    # Verificar que el resultado es una Serie de Pandas
    assert isinstance(aggregated_result, pd.Series)

    # Verificar que los índices son las categorías
    assert 'A' in aggregated_result.index
    assert 'B' in aggregated_result.index
    assert 'C' in aggregated_result.index

    # Verificar los valores agregados (medias)
    # Media para 'A': (10 + 12) / 2 = 11.0
    # Media para 'B': (15 + 18) / 2 = 16.5
    # Media para 'C': 20 / 1 = 20.0
    assert aggregated_result['A'] == 11.0
    assert aggregated_result['B'] == 16.5
    assert aggregated_result['C'] == 20.0

# Se realizan pruebas unitarias para las funciones de procesamiento de datos.
# Se utiliza pytest para ejecutar las pruebas.
# Se utilizan assertions para verificar los resultados esperados.
