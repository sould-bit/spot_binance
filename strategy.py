import pandas as pd
import numpy as np
class test:
    def __init__(self):
        #variables para manejar los datos de compra y venta 
        self.buy_timestamp = []
        self.sell_timestamp = []
        
        
    def log(self,txt, dt = None):
        dt = dt or pd.Timestamp.now()
        print(f"{dt}: {txt}")
        
        
    def costo_promedio(self,lista_compras:list[dict])-> float:
        '''calcula el costo promedio de una lista de compras

            Args:
                lista_compras (list[dict]): Una lista de diccionarios, donde cada diccionario tiene las claves "cantidad" y "precio".

            returns:
                float :el costo promedio de las compras.
        '''
        
        total_invertido = sum(compra["cantidad"] * compra["precio"] for compra in lista_compras)
        total_cantidad = sum(compra["cantidad"] for compra in lista_compras)
        
        costo_promedio = total_invertido / total_cantidad if total_cantidad > 0  else 0
        
        return costo_promedio
        
    def buy(self,price,dia):
        self.buy_timestamp[dia] = price
        self.sell_timestamp[dia] = np.nan
        
    def sell(self,price,dia):
        self.buy_timestamp[dia] = np.nan
        self.sell_timestamp[dia] = price
        
        
    def nan(self,dia):
        self.buy_timestamp[dia] = np.nan
        self.sell_timestamp[dia] = np.nan
        
        