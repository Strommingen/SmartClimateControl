import keys
import network
import urequests
from time import sleep

#def connect():
    # IP='192.168.1.60'
    # SUBNET='255.255.255.0'
    # GATEWAY='192.168.1.1'
    # DNS='0.0.0.0'
    # ap=network.WLAN(network.AP_IF)
    # ap.config(ssid=keys.WIFI_SSID, password=keys.WIFI_PASS)
    # ap.active(True)
    # sleep(0.1)
    # print('1',ap)
    # ap.ifconfig((IP,SUBNET,GATEWAY,DNS))
    # sleep(0.1)
    # print('3', ap)
    # wlan = network.WLAN(network.STA_IF)
    # wlan.active(True)
    # wlan.connect(keys.WIFI_SSID,keys.WIFI_PASS)
    # print(wlan.ifconfig())
    # print(wlan)
    # #Print the html content from google.com
    # print("1. Querying google.com:")
    # r = urequests.get("http://www.google.com")
    # print(r.content)
    # r.close()
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