# USER GUIDE

`FTX - Trading Signal Notify Bot`
- This bot seeks for the coin which has `buying` and `selling` signal & notify user via Line 

Example Message
```
    ZRX/USD : Buy Signal 
    Tread : Up Trend 
    Close Price : 1.111
```

## INSTALLATION GUIDE
- Prequision
  1. Create FTX account & generate API key `https://ftx.com/`
  2. Login to Line and generate Line Token though `https://notify-bot.line.me/`
  3. Clone project respository 

```
    git clone XXXXX.git trading-singal-notify-bot 
```

### Project Environment Setup Guide
1. Install python3 & pip
2. Install required python's packages

```
    pip install -r requirement.txt 
```

3. Copy `.env.example` to `.env`
4. Input API's info and Line Token in `.env` file 
5. How to Run Bot 

```
    python3 main.py
```
