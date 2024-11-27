import matplotlib.pyplot as plt

def generar_grafico(data, tipo="barras"):
    if tipo == "barras":
        plt.bar(data.keys(), data.values())
    elif tipo == "lineas":
        plt.plot(data.keys(), data.values())
    plt.title("Gráfico Estadístico")
    plt.show()
