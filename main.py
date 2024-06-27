from lib import mqtt
import lib.enviorment_util as env
import time
import dht
from machine import Pin
import keys

try:
    ip = env.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

client = mqtt.MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)
client.connect()
print(f"Connected to {keys.AIO_SERVER}")

nextNoticeAction = time.mktime(time.localtime()) # current time since epoch
nextNotice = time.mktime(time.localtime())

# set up pins
led = Pin(15, Pin.OUT)
dhtOutside = dht.DHT11(Pin(17))
dhtInside = dht.DHT11(Pin(14))
windowPin = Pin(27, Pin.IN)

actionNeeded=False

try:
    while True:

        # get all sensor values
        tempOut = env.getTemperature(dhtOutside)
        humOut = env.getHumidity(dhtOutside)

        tempIn = env.getTemperature(dhtInside)
        humIn = env.getHumidity(dhtInside)
        
        windowState=''
        if windowPin.value():
            windowState = 'Open'
        else:
            windowState = 'Closed'

        shouldOpen = env.windowShouldOpen(humOut, humIn, tempOut, tempIn)


        if (shouldOpen == 1 and windowState == 'Closed') or (shouldOpen == -1 and windowState == 'Open'):
            actionNeeded=True
            led.on()
        else:
            actionNeeded=False
            led.off()


        debug=f"Outside {tempOut} C, {humOut} %\nInside {tempIn} C, {humIn} % \nWindow is {windowState}\n\nAction needed?: {actionNeeded} \n\n\n"
        


        # we only send this data every 45 minutes
        if nextNoticeAction - time.mktime(time.localtime()) <= 0:
            if actionNeeded: # and only send to window feed if action is needed
                client.publish(keys.AIO_WINDOW_FEED, windowState)

                nextNoticeAction = time.mktime(time.localtime()) + 2700

        #we send this data every 5 minutes
        if nextNotice - time.mktime(time.localtime()) <= 0:
            client.publish(keys.AIO_TEMPOUT_FEED, str(tempOut))
            client.publish(keys.AIO_TEMPIN_FEED, str(tempIn))
            client.publish(keys.AIO_HUMIN_FEED, str(humIn))
            client.publish(keys.AIO_HUMOUT_FEED, str(humOut))
            client.publish(keys.AIO_DEBUG_FEED, str(debug))

            print('Published!')
            nextNotice = time.mktime(time.localtime()) + 300
        #print(debug)

        time.sleep(10)
finally:
    client.disconnect()
    client = None
    env.disconnect()
    print("Disconnected from Adafruit IO")