#!/usr/bin/python

from modules.TradingSignal import TradingSignal
from modules.LineNotify import LineNotify
from dotenv import dotenv_values

# coin info
pairs     = dotenv_values(".env")['pairs']      # pair coins
timeframe = dotenv_values(".env")['timeframe']  # timeframe : 1m 5m 1h 4h 1d
limit     = dotenv_values(".env")['limit']      # amount of candle sticks
exchange  = dotenv_values(".env")['exchange']

if __name__ == "__main__":
    t = TradingSignal()
    t._login()

    for pair in pairs.split(","):
        try:
            t._getTradingSignal(f"{pair.strip()}-PERP", timeframe, limit)
        except Exception as e:
            print(e)
            LineNotify().sendMessage(f"{pair}-PERP error occured : {e}")
    
# check if bot still running.
# LineNotify().sendMessage(f"{exchange} Bot still running")