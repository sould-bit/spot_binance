#%%
from  binance.spot  import Spot 
from binance.client import  Client as clientt
import config
from pprint import pprint
from time import sleep
import pandas as pd
import numpy as np 
from utils.strategy import indicators
from backtest import grafickrsi, graficticket,plot_rsi
import matplotlib.pyplot as plt


# re realizo pip install pip install TA-Lib, verificar si funciona 
import talib

client = clientt()

class robotBinance: 
    __api = config.api
    __key = config.key
    
    #inicia la seccion con spot binance , da inicio a todas las herramientas del binance 
    BianceClient = Spot(__api,__key)
    Client = Spot(base_url='https://testnet.binance.vision')
   
    
    
    def __init__(self, pair:str,  temporality: str):
        self.pair = pair.upper()
        self.temporality = temporality
        self.symbol = self.pair.removesuffix("USDT")
        
# este metodo hara peticiones , para manejar la exepcion de eero de conection 
    def _request(self, endpoint: str,  parameters: dict = None):
        while True:    
            try:
                response = getattr(self.Client, endpoint)
                
                return response() if parameters is None else response(**parameters)
            except:
                print(f'el endpoint {endpoint} ha fallado .\n parametros {parameters}\n\n')
                sleep(2)
        
    def binanceAcount(self) -> dict :
       
        account = self._request('account')
        
        return account
    
    def criptocurriencies(self) -> list :
        
        
        """
        devuleve una lista con todas las cripto , con saldos positivos  en la cuenta 
        """
        
        return [cripto for cripto in self.binanceAcount().get('balances') if float(cripto.get('free') ) > 0]
        
    def pair_ticket(self, pair:str = None) -> dict:
        """
        devuelve el precio actual del par a dispocicion 
        
        """
        
        symbol = self.pair if pair is None else pair
        
        return float(self._request('ticker_price', {'symbol': symbol.upper()}).get("price"))
        
    def candlestick(self, limit : int = 3000) :
        """
        devuelve un data frame , de velas 
        
        Periodo de tiempo	|  Velas de 15 minutos
        ------------------------------------------
        Día	   ------------>|  96
        Semana ------------>|  672
        Mes	   ------------>|  2.880
        Año	   ------------>|  34.560
        -------------------------------------------
        """
        parametrs = { 'symbol':self.pair,
                      'interval':self.temporality,
                      'limit':limit,
                      }
    
        candle = pd.DataFrame(self._request('klines', parametrs),
                              columns=[
                                  "Open time",
                                  "Open price",
                                  "High price", 
                                  "Low price",
                                  "Close",
                                  "Volume", 
                                  "Kline Close time",
                                  "Quote asset volume",
                                  "Number of trades",
                                  "Taker buy base asset volume",
                                  "Taker buy quote asset volume",
                                  "Unused field, ignore"],
                              dtype=float
                              )

        
        return candle[['Open time','Kline Close time','Open price','High price','Low price','Close','Volume']]
    
    def historical_klines(self,start_time,end_time):
        
        interval = client.KLINE_INTERVAL_15MINUTE
        klines = client.get_historical_klines(symbol=self.pair,interval=interval,start_str=start_time,end_str=end_time)
        data =pd.DataFrame(klines,  columns=
                           ["Open time",
                            "Open", 
                            "High",
                            "Low",
                            "Close",
                            "Volume",
                            "Close time",
                            "Quote asset volume",
                            "Number of trades",
                            "Taker buy base asset volume",
                            "Taker buy quote asset volume", 
                            "Ignore"],
                           dtype=float)
        return data[[ "Open time","Close"]]
        # return [candle for candle in klines]


            
            
            
bot = robotBinance("btcusdt","15m")

#*********************************************************************
            # GRAFICAR  HISTORICAL and rsi
#*********************************************************************
candle_historic = bot.historical_klines("11 Jul, 2023", "30 Aug, 2023")
# candle_historic.index = candle_historic["Open time"]
indicator_rsi = talib.RSI(candle_historic["Close"], timeperiod=14)
# graficticket(candle_historic, 'BTCUSDT')
plot_rsi(candle_historic["Close"],'btcusdt')
#*********************************************************************

#*********************************************************************
            # ordenes

#*********************************************************************

#*********************************************************************

# Este código utiliza un bucle for para recorrer los índices
# de las listas candle_historic e indicator_rsi.
# En cada iteración, se obtienen el precio actual
# y el valor actual del indicador RSI usando los índices correspondientes.
def señal(datos):
    buy_threshold = 30
    sell_threshold = 70
    take_profit_percent = 2
    buy_timestamp = []
    sell_timestamp = []
    compras = 0
    ventas = 0
    on_trade = False
    capital = 100
    earnigns = 0
    take_profit = 0
    cantidad_activos = 0
    stop_loss = -0.5
    for dia in range(len(datos)):
        precio_actual = datos[dia]
        rsi_actual = indicator_rsi[dia]
        # timestamp = candle_historic["Open time"][dia]

        if rsi_actual <= buy_threshold:
            if not on_trade :
                on_trade = True
                compras += 1
                entry_price = precio_actual
                buy_timestamp.append(precio_actual)
                sell_timestamp.append(np.nan)
                # calculamos la cantidad de activos obtenidos con la compra
                cantidad_activos = capital /precio_actual
                # earnigns = 0
                print(f"\n{earnigns}")
            else:
                buy_timestamp.append(np.nan)
                sell_timestamp.append(np.nan)
        
        #  condicion por ganancia  es -1 
        elif on_trade and earnigns <=  stop_loss:

            ventas +=1
            sell_timestamp.append(precio_actual)
            buy_timestamp.append(np.nan)
            on_trade = False
            capital = (cantidad_activos * precio_actual)  + earnigns
            take_profit += earnigns
            # earnigns = 0 
            cantidad_activos = 0
            print(f"earnings {earnigns}")    
            
        # condicion por take profit  +1 
        elif on_trade == True and  earnigns >= take_profit_percent :
            ventas +=1
            sell_timestamp.append(precio_actual)
            buy_timestamp.append(np.nan)
            on_trade = False
            capital = (cantidad_activos * precio_actual)  + earnigns
            cantidad_activos = 0 
            take_profit += earnigns
            print(f"earnings {earnigns}")
            # earnigns = 0 
                
        else:
            buy_timestamp.append(np.nan)
            sell_timestamp.append(np.nan)
        if on_trade:
            earnigns = (precio_actual - entry_price) * cantidad_activos
            
       
                
    print(f"compras\n {compras}\nventas\n{ ventas}\nganancias totales\n{take_profit} \ncapital\n{capital}")
    return (buy_timestamp, sell_timestamp)
    
    
señales = señal(candle_historic["Close"])
señal_v= señales[1]
señal_c = señales[0]
# while len(señal_c) < len(candle_historic):
#     señal_c.append(np.nan)
# while len(señal_v) < len(candle_historic):
#     señal_v.append(np.nan)



candle_historic['compra'] = señal_c
candle_historic['venta'] = señal_v




#*********************************************************************
#   graficar las timestamp de buy and sell
#*********************************************************************

plt.plot(candle_historic["Close"],label="precio")

plt.scatter(candle_historic.index,candle_historic['compra'], marker='^',label='compra', c='g',)
plt.scatter(candle_historic.index,candle_historic['venta'], marker='v',label='venta', c='r')

plt.legend()
plt.title('Compras y Ventas')
plt.xlabel('Tiempo')
plt.ylabel('Precio')
plt.show()



#*********************************************************************
            # GRAFICAR  
#*********************************************************************

# candle = bot.candlestick()['Close']
