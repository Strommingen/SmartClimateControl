from lib import mqtt
import network
import dht
import time
from machine import Pin
import keys

def disconnect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    wlan.disconnect()
    wlan = None

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
# returns 1 if window should open, -1 if it should close, 0 if it does not matter
# def windowShouldOpen(humOut, humIn, tempOut, tempIn) -> int:
#     if (tempOut > 16):
#         # if it is atleast 3 degrees warmer inside and outside is not above 22 return true
#         if ((tempIn - tempOut >= 5) and not (tempOut > 22)) or (humOut > humIn and humIn < 0.4) or (humOut < humIn and humIn > 0.5):
#             return 1
#             # Humidity conditions
#         if tempIn - tempOut <5:
#             return 0
#     # If none of the conditions met, return False
#     return -1

def windowShouldOpen(humOut, humIn, tempOut, tempIn) -> int:
    # Check if the outside temperature is above 16 degrees
    if tempOut > 16:
        # If it's at least 5 degrees warmer inside than outside and outside is not above 22 degrees
        if (tempIn - tempOut >= 5 and tempOut <= 22):
            return 1
        # If outside humidity is greater than inside and inside humidity is less than 40%
        if humOut > humIn and humIn < 0.4:
            return 1
        # If outside humidity is less than inside and inside humidity is greater than 50%
        if humOut < humIn and humIn > 0.5:
            return 1
        # If the temperature difference is less than 5 degrees
        if tempIn - tempOut < 5:
            return 0
    # If none of the conditions are met, the window should remain closed
    return -1

#https://lauryheating.com/ideal-home-humidity/



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


# TODO: here it is black and white if notify or not, but it should not be should be a grey area if tempout > 16 and tempin < 22 it should not matter
        if (shouldOpen == 1 and windowState == 'Closed') or (shouldOpen == -1 and windowState == 'Open'):
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
            nextNotice = time.mktime(time.localtime()) + 2700
        #print(debug)

        time.sleep(10)
finally:
    client.disconnect()
    client = None
    disconnect()
    print("Disconnected from Adafruit IO")