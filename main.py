#%%
from binan import bot_tack
from strategy import test
import numpy as np
import pandas  as pd
from utils.ind import indicators
from plotting import plotingall
import matplotlib.pyplot as plt
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
        #parameters 
        self.on_trade = False
        self.cantidad_activos = 0
        self.total_cantidad_activos = 0
        self.earning = 0
        self.take_profit = 0 
        self.entry_price = 0
        
        
        # counts trades and sells 
        self.trades = []
        self.sells = 0
        
        #data managers
        self.buy_timestamp = []
        self.sell_timestamp = []
        
        #float
    
        
        #int
        self.pnl = 0 
        self.capital  = 0
        self.capital_Final = 0
        
        # data frame 
        self.transations = pd.DataFrame()
        
        
        self.rsi = indicators(self.data).rsi()
        
        # self.transations["sma"] = indicators(self.data).SMA()
        # self.transations["macd"],_,_ = indicators(self.data).macd()
        self.transations["rsi"] = indicators(self.data).rsi()
             
        
    def calcular_antidad_activos_por_precio(self, size):
        '''
        size : espera el tamaño de inversion principal
        '''
        self.cantidad_activos = size / self.current_price
        self.total_cantidad_activos += self.cantidad_activos
        

        
    def next(self, size:int,size_segurity:int, umbral_activation:int,ordenes_seguridad:int,riesgo_seguridad:float, target:float):
        '''
        size : espera el tamaño de inversion principal
        size_segurity : el tamaño , de recompra caunto  riesgo_seguridad sea True
        umbral_activacion : espera el parametro del rsi  ej 30 o 25
        ordenes_seguridad : el numero maximo de ordenes de seguridad  que se pueden cursar  en un ciclo de trading
        riesgo_seguridad : el punto de recompra para promediar 
        target : objetivo take profit en porcentaje
        '''
        # mantenemos la lista para graficar las compras y las ventas  de igual valor a el indice de los datos 
        while len(self.buy_timestamp) < len(self.data):
                self.buy_timestamp.append(np.nan)
        while len(self.sell_timestamp) < len(self.data):
                self.sell_timestamp.append(np.nan)
                
        for dia in range(len(self.data)):
            self.current_price = self.data[dia]
            self.earning = (self.current_price -  self.entry_price) * self.total_cantidad_activos
            porcentage_ganancia = (self.earning / (self.entry_price * self.total_cantidad_activos))*100
    
            if self.transations["rsi"][dia] <= umbral_activation and not self.on_trade:
                self.capital += size
                self.calcular_antidad_activos_por_precio(size=size)
                self.entry_price = self.current_price
                self.trades.append({'cantidad': self.cantidad_activos,'precio': self.current_price})
                self.buy(self.current_price,dia)
                self.on_trade = True
                logging.info(f"el ciclo ha iniciado ")
                self.log("buy: {} \nassets: {}  \n \nto {} rsi  \nzise_buy:{}"
                         .format(self.current_price,self.cantidad_activos,self.rsi[dia],size))
                
            if porcentage_ganancia <= riesgo_seguridad and len(self.trades) < ordenes_seguridad and self.on_trade:
                self.capital += size_segurity
                self.calcular_antidad_activos_por_precio(size=size_segurity)
                self.trades.append({'cantidad': self.cantidad_activos,'precio': self.current_price})
                self.entry_price = self.costo_promedio(self.trades)
                self.earning = (self.current_price -  self.entry_price) * self.total_cantidad_activos
                self.buy(self.current_price,dia)
                self.on_trade = True
                self.log("Rebuy: {} \nassets: {}  \nassets_total: {} \n \nto {} rsi  \n size :{} \n cap: invesment {}"
                         .format(self.current_price,self.cantidad_activos,self.total_cantidad_activos,self.rsi[dia],size_segurity,self.capital))
            # la ganancias en este putno , se calculan con los datos de cierre y no en tiempo
            # real , "si el precio de cierre es - 0.1  lo va a tomar "
            if porcentage_ganancia >= target  and self.on_trade:
                self.sell(self.current_price,dia)
                self.sells += 1
                self.capital_Final = (self.total_cantidad_activos * self.current_price) + self.earning
                self.pnl += self.earning
                self.log("sell: {} with take_profit at {} \n new cap: {}\n".format(self.current_price, self.earning,self.capital_Final))
                logging.info(f"el ciclo ha terminado \n\n start\n\n{self.capital} end {self.capital_Final}\n\n")
                logging.info(f"\nsafety orders:\n {len(self.trades) }\nventas:\n{self.sells}\nganancias totales:\n{self.pnl} \ncapital:\n{self.capital_Final}")
                # inicializar variables 
                self.capital = 0 
                self.trades = []
                self.entry_price = 0
                self.on_trade = False 
                self.total_cantidad_activos = 0
                self.cantidad_activos = 0
                self.earning = 0     
                      
            
if __name__=='__main__':
    bot = bot_tack("BTCUSDT")
    logging.debug(f" ")
    # candle historic trae un data frame 
    candle_historic = bot.candle_history("1 month")
    rsi_estrategy = strate(candle_historic["Close"])


    
    
# print(dir(rsi_estrategy))
# rsi_estrategy.entradas()
    rsi_estrategy.next(size=10,size_segurity=15,umbral_activation=30,ordenes_seguridad=16,riesgo_seguridad=-3,target=2.1)



    candle_historic["compra"] = rsi_estrategy.buy_timestamp

    candle_historic["venta"] = rsi_estrategy.sell_timestamp

          

            
    plotingall(candle_historic)
#*********************************************************************
            # GRAFICAR  HISTORICAL and rsi
#*********************************************************************

# indicator_rsi = indicators(candle_historic.Close).rsi()
# plt.figure(figsize=(12, 6))
# plt.scatter(candle_historic.index,candle_historic["venta"], marker='v',label='venta', c='r')
# plt.scatter(candle_historic.index,candle_historic["compra"], marker='^',label='compra', c='g',)
# plt.plot(candle_historic["Close"],label="precio")

# plt.legend()
# plt.title('Compras y Ventas')
# plt.xlabel('Tiempo')
# plt.ylabel('Precio')
# plt.show()