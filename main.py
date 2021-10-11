#!/usr/bin/python

from modules.TradingSignal import TradingSignal
from modules.LineNotify import LineNotify
from dotenv import dotenv_values

# coin info
pairs     = dotenv_values(".env")['pairs']      # เหรียญที่จะเทรด
timeframe = dotenv_values(".env")['timeframe']  # ช่วงเวลาของกราฟที่จะดึงข้อมูล 1m 5m 1h 4h 1d
limit     = dotenv_values(".env")['limit']      # ให้ดึงข้อมูลมากี่แถว ย้อนหลังกี่แทง

if __name__ == "__main__":
    t = TradingSignal()
    t._login()

    for pair in pairs.split(","):
        try:
            t._getTradingSignal(pair.strip(), timeframe, limit)
        except Exception as e:
            print(e)
            LineNotify().sendMessage(f"{pair} error occured : {e}")
    