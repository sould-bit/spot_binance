#%%
from binance.client import Client
import pandas as pd
from config import _secret , _key
import logging
from time import sleep

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
'''
        Debug :   10
        info:     20
        warning:  30
        error:    40 
        critical: 50 
'''

class bot_tack:
    
        
        
    def __init__(self, pair):
        self.pair = pair.upper()
        
        self.symbol = self.pair.removesuffix("USDT")
        
    def _request(self):
        while True:
            try :
                brok =Client(api_key=_key)
                return brok
            except :
                logging.warning(f"no se ha podido establecer la coneccion con binance Appi")
                sleep(5)
                
    def candle_history(self, start):
        pair  = self.pair
        interval = self._request().KLINE_INTERVAL_5MINUTE
        logging.info(f"intervalo de klines (velas) : {interval}")
        
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
    
    
# bot = bot_tack("BNBUSDT")


# candle_historic = bot.candle_history("1 month")

# candle_historic.info()