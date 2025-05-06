import pandas as pd

def clean_data(df):
    # Elimina valores nulos y duplicados
    df = df.dropna()
    df = df.drop_duplicates()
    return df

def transform_data(df):
    # Cambia el formato de las columnas y crea nuevas columnas
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    return df

def aggregate_data(df):
    # Agrupa los datos por categorías y calcula estadísticas
    grouped_df = df.groupby('category')['value'].mean()
    return grouped_df

# Se realizan funciones para la correcta limpieza y transformación de los datos,
# para que estos puedan ser utilizados por los modelos de machine learning.
