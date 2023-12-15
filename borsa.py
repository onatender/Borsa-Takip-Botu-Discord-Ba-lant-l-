import requests
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Back, Style
import discord

def send_message(mesaj):
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
      channel = client.get_channel(CHANNEL NAME HERE)
      await channel.send(mesaj)
      await client.close()
    client.run("API KEY HERE")
    

class Hisse():
    def __init__(self,hisse_code):
        self.oldValue = 0
        self.newValue = 0
        self.hisse_code = hisse_code
        self.Update()

    def getHisseLink(self):
        return f"https://borsa.doviz.com/hisseler/{self.hisse_code.lower()}"
    
    def getHisseValue(self):
        content = requests.get(self.getHisseLink()).content
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find("div", {"class": "text-xl font-semibold text-white"})
        return element.get_text().replace(',','.')

    def Update(self):
        self.oldValue = self.newValue
        self.newValue = self.getHisseValue()

hisseler = []
with open('data','r',encoding='utf-8') as f:
    for line in f.read().split('\n'):
        if line.strip() != '':
            new_hisse = Hisse(line)
            hisseler.append(new_hisse)

import time
def wait_10_seconds():
    for i in range(10):
        time.sleep(1)

while True:
    for hisse in hisseler:
        hisse.Update()
        text = f"{hisse.hisse_code}:{hisse.oldValue} → {hisse.newValue}"
        if float(hisse.newValue) < float(hisse.oldValue):
            print(Fore.RED,text," hisse düştü")
            send_message(f"@everyone {text}")
        elif float(hisse.newValue) == float(hisse.oldValue):
            print(Fore.WHITE,text," değişiklik yok")
        elif float(hisse.newValue) > float(hisse.oldValue):
            print(Fore.GREEN,text," hisse arttı")
    print(Fore.WHITE,"--------------------------------------------------------------")
    wait_10_seconds()


