
## INSTRALL ON DEBIAN 10 [Google Cloud VM]
---
1. Create VM Instance on Google Cloud 
2. Login to VM Instance 
3. Use following Command 
```
 - sudo apt update
 - python3 -V
 - sudo apt install -y python3-pip
 - sudo apt install python3-pandas
 - sudo apt install git
 - git --version

 - pip3 install ccxt
 - pip3 install python-dotenv
 - pip3 install pandas-ta
```
### Clone Project from Github 
```
- git clone https://github.com/Theeradach/FTX-Trading-Signal-Notify-Bot.git
- cd FTX-Trading-Signal-Notify-Bot
- cp .env.example .env
- sudo vim .env
  - Change API Key & Secret
```

### Install Crontab & Execute Bot on Crontab
```
- sudo apt-get install cron
- crontab -e
- Bot will run at 7:00 and 19:00
```
    0 7-19/12 * * * bash /root/FTX-Trading-Signal-Notify-Bot/runBot.sh > /tmp/ftx-trade-signal-bot.log
```
- sudo service cron restart
```
