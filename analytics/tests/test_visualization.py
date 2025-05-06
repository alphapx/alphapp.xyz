import pytest
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Importar las funciones del archivo visualization.py para probar
from src.visualization import plot_data, plot_time_series # Basado en ejemplo de fuente [4]

# fixture para crear datos de ejemplo para las pruebas de visualización
@pytest.fixture
def sample_dataframe():
    """
    Fixture para crear un DataFrame de Pandas de ejemplo.
    Simula datos de ejemplo adecuados para las funciones de visualización.
    """
    data = {
        'category': ['A', 'B', 'C', 'A', 'B', 'C'],
        'value': [15-20],
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06'])
    }
    df = pd.DataFrame(data)
    return df

# Para probar funciones que llaman plt.show(), a menudo es necesario
# evitar que la ventana de la gráfica aparezca durante las pruebas automatizadas.
# Esto se puede hacer configurando el backend de Matplotlib o mockeando plt.show().
# Aquí usaremos una técnica común para evitar que aparezca la ventana.
# pytest-plt plugin puede ayudar con esto, o configuración manual.
# Por simplicidad, este ejemplo asume que plot_data o plot_time_series
# no abren inmediatamente una ventana o pueden ser testeadas sin interacción visual.
# En un caso real, el uso de Selenium [6] implicaría un entorno de prueba más complejo
# que podría renderizar las visualizaciones para validación visual o de estructura.

def test_plot_data_executes(sample_dataframe):
    """
    Prueba básica para verificar que la función plot_data se ejecuta
    sin errores con datos válidos.
    """
    df = sample_dataframe
    try:
        # Llamar a la función de visualización.
        # Se espera que genere una gráfica (aunque no se muestre).
        plot_data(df)
        # Si la ejecución llega aquí sin excepción, la prueba pasa por ahora.
        # Una prueba más robusta podría verificar el estado de Matplotlib o guardar la figura.
        assert True
    except Exception as e:
        pytest.fail(f"La función plot_data falló con una excepción: {e}")

def test_plot_time_series_executes(sample_dataframe):
    """
    Prueba básica para verificar que la función plot_time_series se ejecuta
    sin errores con datos válidos que incluyen una columna de fecha.
    """
    df = sample_dataframe
    try:
        # Llamar a la función de visualización para series de tiempo.
        plot_time_series(df)
        # Si la ejecución llega aquí sin excepción, la prueba pasa.
        assert True
    except Exception as e:
        pytest.fail(f"La función plot_time_series falló con una excepción: {e}")
