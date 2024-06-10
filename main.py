# main.py -- put your code here!
from library.window import Window
import library.dht11
import dht
from discord_webhook import DiscordWebhook
#https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
from machine import Pin
import keys
import time

pinOutside = Pin(15)
pinInside = Pin(17)
switchPin = Pin(27, Pin.IN)

dhtOutside = dht.DHT11(pinOutside)
dhtInside = dht.DHT11(pinInside)
myWindow = Window(switchPin)

openMessage = "Open your window!"
closeMessage = "Close your window!"
webhook = DiscordWebhook(url=keys.WEBHOOK)

# This will become the time stamp of the last sent notice
lastSent_seconds = 0

while True:

    tempOut = dhtOutside.getTemperature()
    tempIn = dhtInside.getTemperature()

    humOut = dhtOutside.getHumidity()
    humIn = dhtInside.getHumidity()
    
    # Current time
    date = time.localtime() # get the current date as a tuple
    date_seconds = time.localtime(date)# convert the tuple to seconds since last epoch
# check if window should be open
    if (myWindow.TempCompare(tempOut, tempIn) or myWindow.HumidityCompare(humOut, humIn)):
        # if window should be open but is not, notify
        nextNotice = date_seconds + 2700 # number "2700" is 45 minutes in seconds. 45*60=2700
        if not myWindow.IsOpen() and (lastSent > nextNotice):
            webhook.content = openMessage
            webhook.execute()
            lastSent = time.localtime() 
            lastSent_seconds = time.mktime(lastSent) 
    elif (myWindow.IsOpen()) and (lastSent > nextNotice):
        webhook.content = closeMessage
        webhook.execute()
        lastSent = time.localtime()
        lastSent_seconds = time.localtime(lastSent)
    time.sleep(0.2)