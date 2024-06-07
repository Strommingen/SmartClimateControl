# main.py -- put your code here!
from library.window import Window
import library.dht11
import dht
from discord_webhook import DiscordWebhook
#https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
from machine import Pin
import keys
import time
from datetime import datetime, timedelta

pinOutside = Pin(15)
pinInside = Pin(17)
switchPin = Pin(27, Pin.IN)

dhtOutside = dht.DHT11(pinOutside)
dhtInside = dht.DHT11(pinInside)
myWindow = Window(switchPin)

openMessage = "Open your window!"
closeMessage = "Close your window!"
webhook = DiscordWebhook(url=keys.WEBHOOK)
lastSent = datetime(0,0,0)
notifyPeriod = timedelta(0:45:0)

while True:

    tempOut = dhtOutside.getTemperature()
    tempIn = dhtInside.getTemperature()

    humOut = dhtOutside.getHumidity()
    humIn = dhtInside.getHumidity()
    
    date = datetime.now()
# check if window should be open
    if (myWindow.TempCompare(tempOut, tempIn) or myWindow.HumidityCompare(humOut, humIn)):
        # if window should be open but is not, notify
        nextNotice = date + timedelta(minutes=45)
        if not myWindow.IsOpen() and (lastSent > nextNotice):
            webhook.content = openMessage
            webhook.execute()
            lastSent = datetime.now()
    else:
        if (myWindow.IsOpen()) and (lastSent > nextNotice):
            webhook.content = closeMessage
            webhook.execute()
            lastSent = datetime.now()
    time.sleep(0.2)