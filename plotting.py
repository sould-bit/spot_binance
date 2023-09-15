import matplotlib.pyplot as plt
from utils.ind import indicators
import talib as ta
import pandas as pd
import mplfinance as mpf

mpf.__version__

    
def graficticket(date):
    # mpf.plot(date, type='candle', style='charles', title='BTCUSD', ylabel='Precio', figsize=(12, 6))
    
    transations = pd.DataFrame()
    # transations["sma"] = indicators(close["Close"]).SMA()
    # transations["macd"],_,_ = indicators(close).macd()
    transations["rsi"] = indicators(date['Close']).rsi()
    
    # Crear una figura con mpf.figure() y especificar el estilo, el tamaño y el espacio entre subplots
    fig = mpf.figure(style="charles", figsize=(12, 6))
    fig.subplots_adjust(hspace=0.5)

    # Crear tres subplots con fig.add_subplot() y asignarlos a las variables ax1, ax2 y ax3
    ax1 = fig.add_subplot(2, 1, 1) # Primer subplot para el precio de cierre, compra y venta
    ax2 = fig.add_subplot(2, 1, 2) # Segundo subplot para el RSI
    # ax3 = fig.add_subplot(3, 1, 3) # Tercer subplot para el SMA

    # Usar mpf.plot() para graficar el precio de cierre, el tipo de vela, el volumen y el título en el primer subplot (ax1)
    mpf.plot(date, type="candle", volume=True, ax=ax1, axtitle="Precio de Cierre")

    # Usar plt.scatter() para graficar los puntos de compra y venta en el primer subplot (ax1)
    plt.scatter(date.index, date["venta"], marker="v", label="venta", c="r")
    plt.scatter(date.index, date["compra"], marker="^", label="compra", c="g")
    plt.legend()

    # Usar mpf.plot() para graficar el RSI, el tipo de línea y el título en el segundo subplot (ax2)
    mpf.plot(transations["rsi"], type="line", ax=ax2, axtitle="RSI")

    # Usar plt.axhline() para graficar las líneas horizontales de 0 y 30 en el segundo subplot (ax2)
    plt.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
    plt.axhline(y=30, color="red", linestyle="--", linewidth=0.8)

    # Usar mpf.plot() para graficar el SMA, el tipo de línea y el título en el tercer subplot (ax3)
    # mpf.plot(date["SMA"], type="line", ax=ax3, axtitle="SMA")

    # Usar plt.show() para mostrar la figura
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
    transations["rsi"] = indicators(close['Close']).rsi()
    
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
    
    
    
def prueb(date):
    mpf.__version__
    transations = pd.DataFrame()
    # transations["sma"] = indicators(close["Close"]).SMA()
    # transations["macd"],_,_ = indicators(close).macd()
    transations["rsi"] = indicators(date['Close']).rsi()
    line= pd.Series(30,index=date.index)
    
    ap0 = [ mpf.make_addplot(transations['rsi'],color='c',panel=1),
           mpf.make_addplot(date['compra'],type='scatter',marker='^',markersize=100,color='g',label="buy"),  # uses panel 0 by default
           mpf.make_addplot(date['venta'],type='scatter',marker='^',markersize=100,color='r',label="sell"),
           mpf.make_addplot(line, color='r', linestyle='--', panel=1)]  # uses panel 0 by default
         
    mpf.plot(date,type='candle',style='charles' ,panel_ratios=(4,1),addplot=ap0)