import ccxt
import pandas as pd
import pandas_ta as ta
from modules.LineNotify import LineNotify
import emoji
from dotenv import dotenv_values

# .env
apiKey    = dotenv_values(".env")['apiKey']
secret    = dotenv_values(".env")['secret']
password  = dotenv_values(".env")['password']
accountName  = dotenv_values(".env")['accountName']
exchange = dotenv_values(".env")['exchange']

fastEmaLength = int(dotenv_values(".env")['fastEmaLength'])
slowEmaLength = int(dotenv_values(".env")['slowEmaLength'])
rsiLength = int(dotenv_values(".env")['rsiLength'])
BBandsLength = int(dotenv_values(".env")['BBandsLength'])
std = int(dotenv_values(".env")['std'])

class TradingSignal():
    def __init__(self):
        self.exchange   = None
        self.coin       = None
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
        self.rsi = 0
        self.rsiResult = None
        self.MidBBands = 0
        self.BBandsResult = None
        self.position = None

    def _login(self):
        self.exchange = ccxt.ftx({
            'apiKey' : apiKey ,'secret' : secret ,'password' : password ,'enableRateLimit': True
        })
        # Sub Account Check
        if accountName == "" :
            print("\n""Account Name - This is Main Account",': Broker - ', self.exchange)     
        else:
            print( "\n"'Account Name - ', accountName,': Broker - ', self.exchange)
        self.exchange.headers = {'SUBACCOUNT': accountName,}

    def _getTradingSignal(self, pair, timeframe, limit):
        self.__setPairVal(pair, timeframe, limit)
        self.__fetchOhlcv()
        self._getStrategy()
        self.__rsiStatus()
        self.__bbStatus()
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

    def __fetchEMA(self, fast=fastEmaLength, slow=slowEmaLength):
        fastEMA    = self.df_ohlcv.ta.ema(fast)
        slowEMA    = self.df_ohlcv.ta.ema(slow)
        return fastEMA, slowEMA
    
    def __fetchRIS(self, length=rsiLength):
        return self.df_ohlcv.ta.rsi(length=length) 

    def __fetchBBands(self, length=BBandsLength, std=std):
        return self.df_ohlcv.ta.bbands(length=length, std=std) 

    def _getStrategy(self):
        fastEMA, slowEMA = self.__fetchEMA()
        rsi              = self.__fetchRIS()
        bBands           = self.__fetchBBands()
        self.df_ohlcv    = pd.concat([self.df_ohlcv, fastEMA, slowEMA, rsi, bBands], axis=1)

        count = len(self.df_ohlcv)
        self.EMA_fast_A = self.df_ohlcv[f"EMA_{fastEmaLength}"][count-2]  
        self.EMA_fast_B = self.df_ohlcv[f"EMA_{fastEmaLength}"][count-3]

        self.EMA_slow_A = self.df_ohlcv[f"EMA_{slowEmaLength}"][count-2]
        self.EMA_slow_B = self.df_ohlcv[f"EMA_{slowEmaLength}"][count-3]

        self.rsi = round(self.df_ohlcv[f"RSI_{rsiLength}"][count-2], 2)
        self.MidBBands = self.df_ohlcv[f"BBM_{BBandsLength}_{std}.0"][count-2]

        self.closePrice = self.df_ohlcv['close'][count-1]

    def __rsiStatus(self):
        if float(self.rsi) > 70:
            self.rsiResult = "Overbought" 
        elif float(self.rsi) < 30:
            self.rsiResult = "Oversold"
        else: 
            self.rsiResult = None

    def __bbStatus(self):
        if float(self.closePrice) > float(self.MidBBands) :
            self.BBandsResult = "Above Mid"
        else : 
            self.BBandsResult = "Below Mid"

    def __getTrend(self):
        self.trend = "Up Trend" if self.EMA_fast_A > self.EMA_slow_A else "Down Trend"

    def __getSignal(self):
        if (self.EMA_fast_A > self.EMA_slow_A and self.EMA_fast_B < self.EMA_slow_B and
            self.BBandsResult == "Above Mid" and self.rsiResult not in ["Overbought", "Oversold"]):
            self.signal = "Buy Signal"
            self.position = "Long (Buy)"
        elif self.EMA_fast_A < self.EMA_slow_A and self.EMA_fast_B > self.EMA_slow_B:
            self.signal = "Sell Signal"
            self.position = "Short (Sell)"
        else :
            self.signal = "None"

    def __sendLineMsg(self):
        print("\n""####### Signal and Trend #####")
        print("Pair   = ", self.pair)
        print("Trend  = ", self.trend)
        print("Signal = ", self.signal)

        print("\n""####### EMA Report #####")
        print("EMA fast A = ", self.EMA_fast_A)
        print("EMA fast B = ", self.EMA_fast_B)
        print("EMA slow A = ", self.EMA_slow_A)
        print("EMA slow B = ", self.EMA_slow_B)

        print("\n""####### RSI & BBands #####")
        print(f"RSI : {self.rsi} ({self.rsiResult})")
        print(f"BB : {self.BBandsResult}")

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
            \U0001FA99 Symbol : {self.pair}
            Position : {self.position} 
            Exchange : {exchange}
            Trend : {self.trend}
            Time Frame : {self.timeframe}
            Close Price : {self.closePrice}
            RSI : {self.rsi} ({self.rsiResult})
            BB : {self.BBandsResult}
        """
        return message

# if __name__ == "__main__":
#     t = TradingSignal()
#     t._login()
#     t._getTradingSignal()