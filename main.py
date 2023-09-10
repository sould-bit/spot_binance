#%%
from binan import bot_managment
from strategy import test
import numpy as np
import pandas  as pd
from utils.ind import indicators
from plotting import plotingall
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
'''
        Debug :   10
        info:     20
        warning:  30
        error:    40 
        critical: 50 
'''
class strate(test):
    def __init__(self, data):
    
        self.data = data
        # parameters 
        self.on_trade = False
        self.cantidad_activos = 0
        self.total_cantidad_activos = 0
        self.earning = 0
        self.earning_percentage = 0 
        self.entry_price = 0
        
        
        # counts trades and sells 
        self.trades = []
        self.sells = 0
        
        #data managers
        self.buy_timestamp = []
        self.sell_timestamp = []
    
        
        # rendimientos
        self.pnl = 0 
        self.capital  = 0
        self.capital_Final = 0
        
        # data frame 
        self.transations = pd.DataFrame()
        
        
        self.rsi = indicators(self.data).rsi()
        
        # self.transations["sma"] = indicators(self.data).SMA()
        # self.transations["macd"],_,_ = indicators(self.data).macd()
        self.transations["rsi"] = indicators(self.data).rsi()
             
        
    def calcular_antidad_activos_por_precio(self, size: float):
        '''
        Calcula la cantidad de activos basada en el tamaño de inversión principal.

        Args:
            size (float): El tamaño de inversión principal.
        '''
        self.cantidad_activos = size / self.current_price
        self.total_cantidad_activos += self.cantidad_activos
        

        
    def next(self, size:int,size_segurity:int, umbral_activation:int,ordenes_seguridad:int,riesgo_seguridad:float, target:float):
        '''
        Ejecuta la lógica principal de la estrategia de trading DCA (Promediación de Costos).

        Args:
            size (int): Tamaño de la inversión principal.
            size_segurity (int): Tamaño de reinversión cuando el riesgo de seguridad es activado.
            umbral_activacion (int): Umbral del indicador RSI para activar la estrategia (ejemplo: 30 o 25).
            ordenes_seguridad (int): Número máximo de órdenes de seguridad que se pueden realizar en un ciclo de trading.
            riesgo_seguridad (float): Punto de recompra para promediar cuando se activa el riesgo.
            target (float): Objetivo de take profit en porcentaje
        '''
        while len(self.buy_timestamp) < len(self.data):
                self.buy_timestamp.append(np.nan)
        while len(self.sell_timestamp) < len(self.data):
                self.sell_timestamp.append(np.nan)
        logging.info(f"ejecutando la logica")
        
        for dia in range(len(self.data)):
            self.current_price = self.data[dia]
            self.earning = (self.current_price -  self.entry_price) * self.total_cantidad_activos
            porcentage_ganancia = (self.earning / (self.entry_price * self.total_cantidad_activos))*100 if self.total_cantidad_activos > 0 else 0
    
            if self.transations["rsi"][dia] <= umbral_activation and not self.on_trade:
                self.capital += size
                self.calcular_antidad_activos_por_precio(size=size)
                self.entry_price = self.current_price
                self.trades.append({'cantidad': self.cantidad_activos,'precio': self.current_price})
                self.buy(self.current_price,dia)
                self.on_trade = True
                logging.info(f"\n=== El Cliclo ha Iniciado ===\n------------------------------------\nBuy : {self.current_price}\nCantidad de acivos : {self.cantidad_activos}\nTo RSI : {self.rsi[dia]}\nSize Buy : {size}\n------------------------------------")
                
                
            if porcentage_ganancia <= riesgo_seguridad and len(self.trades) < ordenes_seguridad and self.on_trade:
                self.capital += size_segurity
                self.calcular_antidad_activos_por_precio(size=size_segurity)
                self.trades.append({'cantidad': self.cantidad_activos,'precio': self.current_price})
                self.entry_price = self.costo_promedio(self.trades)
                self.earning = (self.current_price -  self.entry_price) * self.total_cantidad_activos
                self.buy(self.current_price,dia)
                self.on_trade = True
                logging.info(f"\n=== Rebuy ===\n------------------------------------\nPrice : {self.current_price}\nAssets : {self.cantidad_activos}\nassets_total: {self.total_cantidad_activos}\nto RSI : {self.rsi[dia]}\nsize : {size_segurity}\ncap : invesment {self.capital}\n------------------------------------")
            # la ganancias en este putno , se calculan con los datos de cierre y no en tiempo
            # real , "si el precio de cierre es - 0.1  lo va a tomar "
            if porcentage_ganancia >= target  and self.on_trade:
                self.sell(self.current_price,dia)
                self.sells += 1
                
                # el capital final , deveria de calcularse sin las ganancias ponderadas , ya que al calcular  el toatl  cantidad de activos ,  es como 
                # recalcular el nuevo capital 
                self.capital_Final = (self.total_cantidad_activos * self.current_price)
                self.pnl += self.earning
                self.earning_percentage += porcentage_ganancia
                

                logging.info(f"\n=== Sell ===\n------------------------------------\nSell : {self.current_price}\nWith a take profit at : {self.earning}\n% : {porcentage_ganancia}\nNew cap : {self.capital_Final}\n------------------------------------")
                logging.info(f"\n\n=== El Cliclo ha Terminado ===\n------------------------------------\nStart : {self.capital}\nEnd : {self.capital_Final}\n------------------------------------")
                logging.info(f"\nSafety orders : {len(self.trades)}\nVentas : {self.sells}\nGanancias por Ciclo : {self.pnl}\nEarning % : {self.earning_percentage}\nCapital : {self.capital_Final}\n------------------------------------\n")
                # inicializar variables 
                self.capital = 0 
                self.trades = []
                self.entry_price = 0
                self.on_trade = False 
                self.total_cantidad_activos = 0
                self.cantidad_activos = 0
                self.earning = 0     
                porcentage_ganancia = 0                      
            
if __name__=='__main__':
    bot = bot_managment("BTCUSDT")
    candle_historic = bot.candle_history("1 month")
    rsi_estrategy = strate(candle_historic["Close"])
    rsi_estrategy.next(size=10,size_segurity=15,umbral_activation=30,ordenes_seguridad=16,riesgo_seguridad=-3,target=2.1)
    candle_historic["compra"] = rsi_estrategy.buy_timestamp
    candle_historic["venta"] = rsi_estrategy.sell_timestamp

    plotingall(candle_historic)