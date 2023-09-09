import matplotlib.pyplot as plt
from utils.ind import indicators
import talib as ta
import pandas as pd



    
def graficticket(date, title):
    plt.plot(date)
    plt.title(title)
    plt.xlabel('time', fontsize=16)
    plt.ylabel(title, fontsize=12)
    #
    
    # Mostrar el gráfico
    
    plt.show()
    
def plot_rsi(close,title):
    # rsi = ta.RSI(close, timeperiod=14)
    rsi = indicators(close)
    plt.plot(rsi, color='purple', linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel(title, fontsize=12)
    plt.ylim(0, 100)  # Establecer límites en el eje y para el RSI
    plt.axhline(30, color='red', linestyle='--', linewidth=1.5)  # Línea horizontal para el nivel de sobreventa
    plt.axhline(70, color='green', linestyle='--', linewidth=1.5)  # Línea horizontal para el nivel de sobrecompra

# Mostrar el gráfico

    plt.show()
    
    
def plotingall(close):
    transations = pd.DataFrame()
    # transations["sma"] = indicators(close["Close"]).SMA()
    # transations["macd"],_,_ = indicators(close).macd()
    transations["rsi"] = indicators(close["Close"]).rsi()
    
    plt.figure(figsize=(12, 6))
    #graficamos el precio y el sma
    plt.subplot(2, 1, 1)
    plt.plot(close["Close"], label='Precio de Cierre', color='blue')
    plt.scatter(close.index,close["venta"], marker='v',label='venta', c='r')
    plt.scatter(close.index,close["compra"], marker='^',label='compra', c='g',)
    # plt.plot(transations["sma"], label=f'SMA (10)', color='orange')
    plt.title('Precios y Media Móvil Simple')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio')
    plt.legend()    
   
    #graficamos el  RSI
    plt.subplot(2, 1, 2)
    plt.plot(transations["rsi"], label='RSI', color='purple')
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.axhline(y=30, color='red', linestyle='--', linewidth=0.8)
    plt.legend()
    plt.tight_layout()
    plt.show()