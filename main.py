from library import window, mqtt, dht11, adaWhook
from library.adaWhook import sub_cb, AdaWebhook
import library.discordWhook as whook
import dht, time
from machine import Pin
import keys

lastSent_seconds = 0

pinOutside = Pin(15)
pinInside = Pin(17)
togglePin = Pin(27, Pin.IN)

dhtOutside = dht.DHT11(pinOutside)
dhtInside = dht.DHT11(pinInside)
myWindow = window.Window(togglePin)

openMessage = "Open your window!"
closeMessage = "Close your window!"

client = mqtt.MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)

adaHumIn = AdaWebhook(keys.AIO_HUMIN_FEED, client)
adaHumOut = AdaWebhook(keys.AIO_HUMOUT_FEED, client)
adaTempIn = AdaWebhook(keys.AIO_TEMPIN_FEED, client)
adaTempOut = AdaWebhook(keys.AIO_TEMPOUT_FEED, client)
adaWindow = AdaWebhook(keys.AIO_WINDOW_FEED, client)

client.set_callback(sub_cb)
client.connect()
client.subscribe(keys.AIO_WINDOW_FEED)

print("Connected to %s, subscribed to %s topic" % (keys.AIO_SERVER, keys.AIO_WINDOW_FEED))

# This will become the time stamp of the last sent notice
try:
    while True:
        client.check_msg()
        tempOut = dht11.getTemperature(dhtOutside)
        humOut = dht11.getHumidity(dhtOutside)

        tempIn = dht11.getTemperature(dhtInside)
        humIn = dht11.getHumidity(dhtInside)
        
    # Current time
        date = time.localtime() # get the current date as a tuple
        date_seconds = time.mktime(date)# convert the tuple to seconds since last epoch
        nextNotice = date_seconds + 2700 # number "2700" is 45 minutes in seconds. 45*60=2700

        isNotified = None
    # check if window should be open
        if myWindow.tempShouldOpen(tempOut, tempIn) or myWindow.humidShouldOpen(humOut, humIn):
            # if window should be open but is not, notify
            if not myWindow.IsOpen() and (lastSent_seconds > nextNotice):
                whook.notify()
                isNotified=True
                lastSent = time.localtime() 
                lastSent_seconds = time.mktime(lastSent) 
        elif (myWindow.IsOpen()) and (lastSent_seconds > nextNotice):
            whook.notify()
            isNotified=True
            lastSent = time.localtime()
            lastSent_seconds = time.localtime(lastSent)
        time.sleep(2)
        adaTempOut.publish(tempOut, isNotified)
        adaTempIn.publish(tempIn, isNotified)
        adaHumOut.publish(humOut, isNotified)
        adaHumIn.publish(humIn, isNotified)

        print(f'Outside {tempOut} C, {humOut} %')
        print(f'Inside {tempIn} C, {humIn} %')
        print(f'Window is open: ', myWindow.IsOpen())
finally:
    client.disconnect()
    client = None
    print("Disconnected from Adafruit IO")