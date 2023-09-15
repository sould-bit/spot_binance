#%%
from binance.client import Client
import pandas as pd
from config import _secret , _key
import logging
from time import sleep
import mplfinance as mpl

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
'''
        Debug :   10
        info:     20
        warning:  30
        error:    40 
        critical: 50 
'''

class bot_managment:
    
        
        
    def __init__(self, pair):
        self.pair = pair.upper()
        
        self.symbol = self.pair.removesuffix("USDT")
        
    def _request(self):
        while True:
            try :
                brok =Client(api_key=_key)
                logging.info(f"iniciando coneccion con la Api: ")
                return brok
            except :
                logging.warning(f"no se ha podido establecer la coneccion con binance Appi")
                sleep(5)
                
    def candle_history(self, start):
        '''
        carga los datos , y simula un  mercado en vivo  con velas de cierre de 1 minuto
        
        Args:
            start(str): el tiempo para cargar los datos  ej 1 month, 2 month etc
            Interval_rsi: el umbral de rsi que se quiere obtener[30,15,5,1]\n
            ejemplo 
            para 1 mes quieres cargar , el rsi de una temporalidad de 15 minuto ('15'),
            o una temporalidad de de  5 minutos ('5')
        
        
        
        WARNING :
            este metodo no simula un entorno 100 % real de mercado en vivo 
        '''
        
        pair  = self.pair
        interval = self._request().KLINE_INTERVAL_1MINUTE   
        logging.info(f"intervalo de datos (velas) : {interval}")
        
        kline = self._request().get_historical_klines(symbol=pair,interval=interval,start_str=start)
        data = pd.DataFrame(kline,columns=["Open t",
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
                                                "ignore"],
                                                 dtype=float)
        data["Open t"] = pd.to_datetime(data["Open t"],unit="ms")

        data.set_index("Open t", inplace=True)
        return data
    
     
# bot = bot_managment("BTCUSDT")
# candle_historic = bot.candle_history("1 month")
# # Agregar líneas de tendencia para los altos y bajos
# # mpl.plot(candle_historic, type='candle', style='charles', title='Gráfico de Velas con Líneas de Tendencia', ylabel='Precio', figsize=(10, 6))
