import requests
from dotenv import dotenv_values

# .env 
token = dotenv_values(".env")['lineToken']

class LineNotify():
    def __init__(self):
        self.url = 'https://notify-api.line.me/api/notify'
        self.headers = {
            'content-type':'application/x-www-form-urlencoded',
            'Authorization':'Bearer ' + token
        }
        
    def sendMessage(self, msg):
        r = requests.post(self.url, headers=self.headers, data = {'message':msg})
        print (r.text)