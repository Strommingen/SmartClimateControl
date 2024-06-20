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

def windowShouldOpen(humOut, humIn, tempOut, tempIn) -> bool:
    if (tempOut >= 17) and (tempIn >= 24) and (tempOut > tempIn):
        return True
        # Humidity conditions
    if (humOut > humIn and humIn < 0.4) or (humOut < humIn and humIn > 0.5):
        return True
    # If none of the conditions met, return False
    return False
#https://lauryheating.com/ideal-home-humidity/


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

nextNotice = time.mktime(time.localtime()) # current time since epoch

led = Pin(14, Pin.OUT)
dhtOutside = dht.DHT11(Pin(15))
dhtInside = dht.DHT11(Pin(17))
windowPin = Pin(27, Pin.IN)
actionNeeded=False

try:
    while True:

        # get all sensor values
        tempOut = getTemperature(dhtOutside)
        humOut = getHumidity(dhtOutside)

        tempIn = getTemperature(dhtInside)
        humIn = getHumidity(dhtInside)
        
        windowState=''
        if windowPin.value():
            windowState = 'Open'
        else:
            windowState = 'Closed'

        shouldOpen = windowShouldOpen(humOut, humIn, tempOut, tempIn)

        if (shouldOpen and windowState == 'Closed') or (not shouldOpen and windowState == 'Open'):
            actionNeeded=True
            led.on()
        else:
            actionNeeded=False
            led.off()


        debug=f"Outside {tempOut} C, {humOut} %\nInside {tempIn} C, {humIn} % \nWindow is {windowState}\n\nAction needed?: {actionNeeded} \n\n\n"
        


        # we only send data every 45 minutes
        if nextNotice-time.mktime(time.localtime()) < 0:
            if actionNeeded: # and only send to window feed if action is needed
                client.publish(keys.AIO_WINDOW_FEED, windowState)
            client.publish(keys.AIO_TEMPOUT_FEED, str(tempOut))
            client.publish(keys.AIO_TEMPIN_FEED, str(tempIn))
            client.publish(keys.AIO_HUMIN_FEED, str(humIn))
            client.publish(keys.AIO_HUMOUT_FEED, str(humOut))
            client.publish(keys.AIO_DEBUG_FEED, str(debug))

            print('Published!')
            nextNotice = time.mktime(time.localtime()) +1001
        print(debug)

        # print(f'Outside {tempOut} C, {humOut} %')
        # print(f'Inside {tempIn} C, {humIn} %')
        # print(f'Window is {windowState}')
        # print(f'Action needed?: {actionNeeded}')
        # print(f'Time until next publish: {nextNotice-time.mktime(time.localtime())} \n')


        time.sleep(10)
finally:
    client.disconnect()
    client = None
    wifiConnection.disconnect()
    print("Disconnected from Adafruit IO")