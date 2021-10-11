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


## INSTRALL ON DEBIAN 10 [Google Cloud VM]
---
1. Create VM Instance on Google Cloud 
2. Login to VM Instance 
3. Use following Command 

 - sudo apt update
 - python3 -V
 - sudo apt install -y python3-pip
 - sudo apt install python3-pandas
 - sudo apt install git
 - git --version

 - pip3 install ccxt
 - pip3 install python-dotenv
 - pip3 install pandas-ta

### Clone Project from Github 
- git clone https://github.com/Theeradach/FTX-Trading-Signal-Notify-Bot.git
- cd FTX-Trading-Signal-Notify-Bot
- cp .env.example .env
- sudo vim .env
  - Change API Key & Secret


### Install Crontab 
- sudo apt-get install cron
- crontab -e
```
    */2 * * * * /usr/bin/python3 /home/jackky1929/FTX-Trading-Signal-Notify-Bot/main.py > /tmp/trading-bot.log 
```
- sudo service cron restart