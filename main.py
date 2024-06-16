from lib import window, mqtt, wifiConnection
import dht
import time
from machine import Pin
import keys


def getTemperature(sensor) -> float:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        return temperature
    except Exception as err:
        print("Something went wrong while reading temperature..", err)

def getHumidity(sensor) -> float:
    try:
        sensor.measure()
        humidity = sensor.humidity()
        return humidity
    except Exception as err:
        print("Something went wrong while reading humidity..", err)

# Function used for debugging. Callback when subscribed message arrives.
# def sub_cb(topic, msg) -> None:
#     print((topic, msg))

try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

client = mqtt.MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)
#client.set_callback(sub_cb)
client.connect()
print(f"Connected to {keys.AIO_SERVER}")

lastSent_seconds = 2700


dhtOutside = dht.DHT11(Pin(15))
dhtInside = dht.DHT11(Pin(17))
myWindow = window.Window(Pin(27, Pin.IN))

try:
    while True:
        # get all sensor values
        tempOut = getTemperature(dhtOutside)
        humOut = getHumidity(dhtOutside)

        tempIn = getTemperature(dhtInside)
        humIn = getHumidity(dhtInside)
        
    # Gets the current time and adds 45 minutes 
        date = time.localtime()
        nextNotice = time.mktime(date) + 2700
#TODO: make the window value only send when action needs to be taken

    # check if window should be open
        if myWindow.tempShouldOpen(tempOut, tempIn) or myWindow.humidShouldOpen(humOut, humIn):
            # if window should be open but is not, change the message
            if not myWindow.IsOpen() and (lastSent_seconds > nextNotice):
                client.publish(keys.AIO_WINDOW_FEED, 'Closed')
                print('Notified!')

        # if window should not be open but is, change message
        elif (myWindow.IsOpen()) and (lastSent_seconds > nextNotice):
            client.publish(keys.AIO_WINDOW_FEED, 'Open')
            print('Notified!')

        # we only send data every -- minutes
        if lastSent_seconds > nextNotice:
            client.publish(keys.AIO_TEMPOUT_FEED, str(tempOut))
            client.publish(keys.AIO_TEMPIN_FEED, str(tempIn))
            client.publish(keys.AIO_HUMIN_FEED, str(humIn))
            client.publish(keys.AIO_HUMOUT_FEED, str(humOut))
            print('Published!')
            lastSent = time.localtime() 
            lastSent_seconds = time.mktime(lastSent)

        print(f'Outside {tempOut} C, {humOut} %')
        print(f'Inside {tempIn} C, {humIn} %')
        print(f'Window is open: ', myWindow.IsOpen())

        time.sleep(30)
finally:
    client.disconnect()
    client = None
    wifiConnection.disconnect()
    print("Disconnected from Adafruit IO")