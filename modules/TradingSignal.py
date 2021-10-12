import ccxt
import pandas as pd
import pandas_ta as ta
from modules.LineNotify import LineNotify
from dotenv import dotenv_values

# .env
apiKey    = dotenv_values(".env")['apiKey']
secret    = dotenv_values(".env")['secret']
password  = dotenv_values(".env")['password']
Account_name  = dotenv_values(".env")['accountName']
exchange  = dotenv_values(".env")['exchange']

class TradingSignal():
    def __init__(self):
        self.exchange   = None
        self.pair       = None
        self.timeframe  = None
        self.limit      = None
        self.df_ohlcv   = None
        self.trend      = None
        self.signal     = None
        self.EMA_fast_A = 0
        self.EMA_fast_B = 0
        self.EMA_slow_A = 0
        self.EMA_slow_B = 0
        self.closePrice = 0

    def _login(self):
        self.exchange = ccxt.ftx({
            'apiKey' : apiKey ,'secret' : secret ,'password' : password ,'enableRateLimit': True
        })
        # Sub Account Check
        if Account_name == "" :
            print("\n""Account Name - This is Main Account",': Broker - ', self.exchange)     
        else:
            print( "\n"'Account Name - ',Account_name,': Broker - ', self.exchange)
        self.exchange.headers = {'ftx-SUBACCOUNT': Account_name,}

    def _getTradingSignal(self, pair, timeframe, limit):
        self.__setPairVal(pair, timeframe, limit)
        self.__fetchOhlcv()
        self.__fetchEMA()
        self.__getTrend()
        self.__getSignal()
        self.__sendLineMsg()

    def __setPairVal(self, pair, timeframe, limit):
        self.pair = pair
        self.timeframe = timeframe
        self.limit = int(limit)
    
    def __fetchOhlcv(self):
        # fetch data from exchange
        self.df_ohlcv  = self.exchange.fetch_ohlcv(self.pair, timeframe=self.timeframe, limit=self.limit)
        self.df_ohlcv  = pd.DataFrame(self.df_ohlcv, columns =['datetime', 'open','high','low','close','volume'])
        # convert timestamp format to datetime Pandas
        self.df_ohlcv['datetime']  = pd.to_datetime(self.df_ohlcv['datetime'], unit='ms')
        # print("\n""results : " "\n", self.df_ohlcv)

    def __fetchEMA(self, fast=13, slow=33):
        EMA_fast    = self.df_ohlcv.ta.ema(fast)
        EMA_slow    = self.df_ohlcv.ta.ema(slow)
        self.df_ohlcv    = pd.concat([self.df_ohlcv, EMA_fast, EMA_slow], axis=1)

        count = len(self.df_ohlcv)
        self.EMA_fast_A = self.df_ohlcv['EMA_13'][count-2]  
        self.EMA_fast_B = self.df_ohlcv['EMA_13'][count-3]

        self.EMA_slow_A = self.df_ohlcv['EMA_33'][count-2]
        self.EMA_slow_B = self.df_ohlcv['EMA_33'][count-3]

        print("\n""####### EMA Report #####")
        print("EMA fast A = ", self.EMA_fast_A)
        print("EMA fast B = ", self.EMA_fast_B)
        print("EMA slow A = ", self.EMA_slow_A)
        print("EMA slow B = ", self.EMA_slow_B)

        self.closePrice = self.df_ohlcv['close'][count-1]

    def __getTrend(self):
        self.trend = "Up Trend" if self.EMA_fast_A > self.EMA_slow_A else "Down Trend"

    def __getSignal(self):
        if self.EMA_fast_A > self.EMA_slow_A and self.EMA_fast_B < self.EMA_slow_B:
            self.signal = "Buy Signal"
        elif self.EMA_fast_A < self.EMA_slow_A and self.EMA_fast_B > self.EMA_slow_B:
            self.signal = "Sell Signal"

    def __sendLineMsg(self):
        print("\n""####### Signal and Trend #####")
        print("Exchange = ", exchange)
        print("Pair   = ", self.pair)
        print("Trend  = ", self.trend)
        print("Signal = ", self.signal)

        print("\n""####### Trade Status #####")
        if self.signal  == "Buy Signal" :
            print("BUY-Trade")
            message = self.__genMessage()
            LineNotify().sendMessage(message)
            
        elif self.signal  == "Sell Signal" :
            print("SELL-Trade")
            message = self.__genMessage()
            LineNotify().sendMessage(message)

        else :
            print("Non-Trade")
        
    def __genMessage(self) -> str:
        message = f"""
            {self.pair} : {self.signal}
            Exchange : {exchange}
            Trend : {self.trend}
            Time Frame : {self.timeframe}
            Close Price : {self.closePrice}
        """
        return message

# if __name__ == "__main__":
#     t = TradingSignal()
#     t._login()
#     t._getTradingSignal()
