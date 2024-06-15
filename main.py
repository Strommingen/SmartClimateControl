from library import window, mqtt, dht11, wifiConnection
from library.adaWhook import sub_cb, AdaConnection
import library.discordWhook as whook
import dht, time
from machine import Pin
import keys
from machine import WDT

# wdt = WDT(timeout=8000)..
try:
    # wdt.feed()
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# def http_get(url = 'http://detectportal.firefox.com/'):
#     import socket                           # Used by HTML get request
#     import time                             # Used for delay
#     _, _, host, path = url.split('/', 3)    # Separate URL request
#     addr = socket.getaddrinfo(host, 80)[0][-1]  # Get IP address of host
#     s = socket.socket()                     # Initialise the socket
#     s.connect(addr)                         # Try connecting to host address
#     # Send HTTP request to the host with specific path
#     s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))    
#     time.sleep(1)                           # Sleep for a second
#     rec_bytes = s.recv(10000)               # Receve response
#     print(rec_bytes)                        # Print the response
#     s.close()                               # Close connection
# #z
# try:
#     # wdt.feed()
#     http_get()
# except (Exception, KeyboardInterrupt) as err:
#     print("No Internet", err)

lastSent_seconds = 0

pinOutside = Pin(15)
pinInside = Pin(17)
togglePin = Pin(27, Pin.IN)

dhtOutside = dht.DHT11(pinOutside)
dhtInside = dht.DHT11(pinInside)
myWindow = window.Window(togglePin)

# openMessage = "Open your window!"
# closeMessage = "Close your window!"

client = mqtt.MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)

adaHumIn = AdaConnection(keys.AIO_HUMIN_FEED, client)
adaHumOut = AdaConnection(keys.AIO_HUMOUT_FEED, client)
adaTempIn = AdaConnection(keys.AIO_TEMPIN_FEED, client)
adaTempOut = AdaConnection(keys.AIO_TEMPOUT_FEED, client)
adaWindow = AdaConnection(keys.AIO_WINDOW_FEED, client)

client.set_callback(sub_cb)
client.connect()

print("Connected to %s, subscribed to %s topic" % (keys.AIO_SERVER, keys.AIO_WINDOW_FEED))

isNotified = None

# This will become the time stamp of the last sent notice
try:
    while True:
        # wdt.feed()
        client.check_msg()
        tempOut = dht11.getTemperature(dhtOutside)
        humOut = dht11.getHumidity(dhtOutside)

        tempIn = dht11.getTemperature(dhtInside)
        humIn = dht11.getHumidity(dhtInside)
        
    # Current time
        date = time.localtime() # get the current date as a tuple
        date_seconds = time.mktime(date)# convert the tuple to seconds since last epoch
       # nextNotice = date_seconds + 2700 # number "2700" is 45 minutes in seconds. 45*60=2700
        nextNotice = -1
    # check if window should be open
        if myWindow.tempShouldOpen(tempOut, tempIn) or myWindow.humidShouldOpen(humOut, humIn):
            # if window should be open but is not, notify
            if not myWindow.IsOpen() and (lastSent_seconds > nextNotice):
                adaWindow.publish("Open")
                isNotified=True
                lastSent = time.localtime() 
                lastSent_seconds = time.mktime(lastSent) 
        elif (myWindow.IsOpen()) and (lastSent_seconds > nextNotice):
            adaWindow.publish("Close")
            isNotified=True
            lastSent = time.localtime()
            lastSent_seconds = time.mktime(lastSent)
        time.sleep(2)
        adaTempOut.publish(tempOut, isNotified=isNotified)
        adaTempIn.publish(tempIn, isNotified=isNotified)
        adaHumOut.publish(humOut, isNotified=isNotified)
        adaHumIn.publish(humIn, isNotified=isNotified)

        print(f'Outside {tempOut} C, {humOut} %')
        print(f'Inside {tempIn} C, {humIn} %')
        print(f'Window is open: ', myWindow.IsOpen())
finally:
    client.disconnect()
    client = None
    wifiConnection.disconnect()
    print("Disconnected from Adafruit IO")