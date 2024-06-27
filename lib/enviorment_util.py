import network
import keys
import dht
from time import sleep

def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip

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


def windowShouldOpen(humOut, humIn, tempOut, tempIn) -> int:
    # Check if the outside temperature is above 16 degrees
    if tempOut > 16 and tempOut < 26:
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