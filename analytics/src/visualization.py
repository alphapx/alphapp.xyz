import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(df):
    # Crea un gráfico de barras
    sns.barplot(x='category', y='value', data=df)
    plt.show()

def plot_time_series(df):
    # Crea un gráfico de líneas
    plt.plot(df['date'], df['value'])
    plt.show()

# Se crean las gráficas necesarias para poder analizar de mejor manera la información de los usuarios.
