import talib  as ta



class indicators:
    
    def __init__(self, data):
        self.close = data.get('Close')
        self.open = data.get('Open price')
        self.high = data.get('High price')
        
        
        
    def ema(self):
        return ta.EMA(self.close, timeperiod=15).iloc[-1]

    
    def rsi(self):
        return ta.RSI(self.close, timeperiod=14)
    
    

        
        
        
        
    
    

    