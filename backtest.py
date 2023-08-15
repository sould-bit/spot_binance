import matplotlib.pyplot as plt
import binance
import talib as ta


def grafickrsi(date, title):
    # Graficar el RSI con estilo de trading view
    plt.plot(date, color='purple', linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel(title, fontsize=12)
    plt.ylim(0, 100)  # Establecer límites en el eje y para el RSI
    plt.axhline(30, color='red', linestyle='--', linewidth=1.5)  # Línea horizontal para el nivel de sobreventa
    plt.axhline(70, color='green', linestyle='--', linewidth=1.5)  # Línea horizontal para el nivel de sobrecompra

    # Mostrar el gráfico
    # fig, ax = plt.subplots(figsize=(15, 10))

    # Plot the RSI

    # ax.plot(date, color='purple', linewidth=2)
    plt.show()
    
def graficticket(date, title):
    plt.plot(date)
    plt.title(title)
    plt.xlabel('time', fontsize=16)
    plt.ylabel(title, fontsize=12)
    #
    
    # Mostrar el gráfico
    
    plt.show()
    
def plot_rsi(close,title):
    rsi = ta.RSI(close, timeperiod=14)
    plt.plot(rsi, color='purple', linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel(title, fontsize=12)
    plt.ylim(0, 100)  # Establecer límites en el eje y para el RSI
    plt.axhline(30, color='red', linestyle='--', linewidth=1.5)  # Línea horizontal para el nivel de sobreventa
    plt.axhline(70, color='green', linestyle='--', linewidth=1.5)  # Línea horizontal para el nivel de sobrecompra

# Mostrar el gráfico

    plt.show()
    