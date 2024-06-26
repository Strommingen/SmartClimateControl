# Smart Climate Control System For A Window

[![hackmd-github-sync-badge](https://hackmd.io/ZVxbMHrCR8-jHQ3t1b0l-g/badge)](https://hackmd.io/ZVxbMHrCR8-jHQ3t1b0l-g)


    Author: Gustaf Nordlander (gn222ia)
**Overview:** This tutorial will show you how to make a smart climate control system in the form of a system that measures values outdoors and indoors. The system notifies that an action needs to be taken, the window it is attached to needs to close or open to effectivly regulate the climate indoors.

Please note that the tutorial is based on having Windows as the operating system.


Expect around - hours

## Objective
During the summer it can be difficult regulating temperature inside your home. Energy consumtion can increase with the use of fans or AC's. A simple way to help lower the use of these potentially powerhungry electronics is to open your window when it is colder outside and close it when it is hotter. For some, meaning me, it can be difficult to remember to do this and to make a habit  of it. 

The data generated from this IoT device can contribute to a better understanding of the climate inside the home or other indoor space the device is implemented in. This can help the user understand if there is a bigger problem that simply opening and closing a window at the appropriate times cannot solve. 

## Materials
The components used in this project was bought from [Electrokit.com](https://www.electrokit.com/)

| Component                  | Article Number | Price (SEK) |
| -------------------------- | -------------- | ----------- |
| Raspberry pi Pico WH       | 41019114       | 109 kr      |
| USB-cabel                  | 41003290       | 39 kr       |
| DHT11 sensor*              | 41015728       | 49 kr       |
| Digital Hall Sensor        | 41015730       | 39 kr       |
| Magnet Neo35               | 41011480       | 11 kr       |
| Breadboard 840 connections | 10160840       | 69 kr       |
| Red LED | 40307020       | 5 kr       |
| Resistor 3W 4.7kohm 5% (4k7) | 41011689       | 6 kr       |

**Please note: Two DHT11 was used in this project.*

The Pico WH microcontroller used is a good starting point for a IoT project if you have no prior experience with building an IoT device in my opinion. It has wifi capabilities so many simple projects that you might want to make in your apartment are possible.



## Computer Setup
### Flash the firmware
To operate the microcontroller you will need the micropython firmware.
Follow these steps to flash the firmware onto your Pico WH:
1. Download the micropython firmware which you will find on the [micropython](https://www.micropython.org/download/RPI_PICO_W/) website.
2. While holding down the BOOTSEL button on the Pico WH plug it in to your computer.
3. You should now see the microcontroller as a USB drive on the computer.
4. Simply drag the firmware file to the USB drive to copy it onto the Pico WH. The USB drive should now disapear wich means the process was successfully done.
### IDE
Visual Studio Code was my choice of IDE to program the Pico WH microcontroller due to prior experience with the IDE. It has a large community that supports it with many different plugins making it a diverse IDE.

1. Install [Visual Studio Code](https://code.visualstudio.com/). Click the arrow next to the download button for download links to more operating systems.
2. Next you need to install [Node.js](https://nodejs.org/en/).
3. Now open Visual Studio Code and the extension manager in the left side panel.
4. Search for Pymakr and install it (Node.js is needed for this plugin).

With Pymakr installed you can now update the microcontroller live by enabling development mode on the device. The makers of Pymakr have a brief overview of this [here.](https://github.com/sg-wireless/pymakr-vsc/blob/HEAD/GET_STARTED.md) You simply need to save the code with the microcontroller connected to your computer and development mode enabled. This will update the software on the Pico.

## Putting everything together
Using the breadboard we connect all our sensors to the Pico WH. Make sure the microcontroller is not plugged in to any power source during this step. Be advised to follow the image below when putting everything together, if other pins are used, be sure to update the code. 
<img src="https://hackmd.io/_uploads/Skt1liYL0.png"
     alt="Visual representation of breadboard setup" />

The red wiring indicates power wiring, blue indicates ground wiring and yellow is the data wiring.

## Platform
[Adafruit IO](https://io.adafruit.com/) was used for the project. It is a fairly simple platform and straightforward to use and suitible for a small scale project like this. There are versions of it that you can use, I used the free version which allows for 10 feeds and 30 messages per minute. The data is also stored for 30 days which is good for the scope of the course to which this project belongs to. Here you can also utilize their "actions" section that works like an if-statement. So if a datapoint is recieved from a feed that contains a specific value, Adafruit will take an action that you specified. I implemented a webhook with this to send me a message in discord if I need to close or open a window. 

While Adafruit is a great platform I want to add that if I had a little more time I would have been going the TIG stack route. The limited feeds and 30 messages were not an issue for my project but the Actions section was. It was a bit limiting since you cannot make that complex decicions. Also the 30 day limit to storage is limiting so if you intend to use the data for anything like machine learning or just statistics I would not recommend this platform.

## Code
All code is written in micropython. The libraries used are listed :
* 

For the program to work a file must be added named keys.py in the root folder. And use this template to populate the file, adding the correct values.
```
import machine
import ubinascii

WIFI_SSID = '' # WIFI SSID
WIFI_PASS = '' # WIFI PASSWORD

AIO_SERVER = "" # ADAFRUIT IO SERVER
AIO_PORT = #PORT USED
AIO_USER = "" # ADAFRUIT USERNAME
AIO_KEY = "" # ADAFRUIT KEY
AIO_TEMPOUT_FEED = "" # ADAFRUIT TEMPERATURE OUTSIDE FEED
AIO_TEMPIN_FEED ="" # ADAFRUIT TEMPERATURE INSIDE FEED
AIO_HUMOUT_FEED = "" # ADAFRUIT HUMIDITY OUTSIDE FEED
AIO_HUMIN_FEED = "" # ADAFRUIT HUMIDITY INSIDE FEED
AIO_WINDOW_FEED="" # ADAFRUIT WINDOW FEED
AIO_DEBUG_FEED="" # ADAFRUIT DEBUG FEED
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id()) # CLIENT ID
```

The function that controls if a window should open or not takes into account the humidity and temperature inside and outside.

```
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
```

It returns 1 if the window should open, -1 if it should not (so it should be closed) and 0 if it does not matter. And it will always return -1 if the temperature outside is below 16 degrees. Originally this was a bool function that returned true or false but after letting the microcontroller run for a while I found that I needed a "grey-area". 

For the humidity comparisions I found an [article](https://lauryheating.com/ideal-home-humidity/) where it is stated that the recommended hudity levels should be between 40-60% altough 50% was better as a maximun so that is the value used in the code. They state more complex conditions as to where the humidity percentage should be if temperature is also considered. This was however not implemented as the humidity was viewed by me as a secondary consideration and the main problem in my apartment is the temperature regulation. 

In the main loop of the program we read the value from the Hall Sensor to see the current state the window is in. Then we determine what state the window *should* be in.

```
        if windowPin.value():
            windowState = 'Open'
        else:
            windowState = 'Closed'

        shouldOpen = windowShouldOpen(humOut, humIn, tempOut, tempIn)


        if (shouldOpen == 1 and windowState == 'Closed') or (shouldOpen == -1 and windowState == 'Open'):
            actionNeeded=True
            led.on()
        else:
            actionNeeded=False
            led.off()
```

We then determine if an action is needed or not and with that we also turn on/off our visual indicator.


## Transmitting the data/connectivity
There are two different time frames for publishing the data. Every 45 minutes for the window feed where we send the current state of the window, if an action is needed. And every 5 minutes for all other feeds.
```
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

            nextNotice = time.mktime(time.localtime()) + 300
```
After data is published in either group the "nextNotice" or "nextNoticeAction" variable is reset. 

Now to actually transmit the data captured on the device to Adafruit IO I used WIFI and MQTT. WIFI was convenient considering the device will be in my home and my router is pretty much always on. The Pico WH also has inbuilt WIFI capabilities making it a good choice. Now the energy consumption would be better if LoRaWAN was used but considering the location it is easily maintained at least, I can charge the powerbank I will use to power the device easily.

When the device is powered the first thing it does is connect to WIFI. It also connects to a MQTT broker, in this case it is hosted on Adafruit IO. From here we can publish to our feeds (topics) established in Adafruit IO.

As previously mentioned I utilized the actions in Adafruit IO send messages to discord when I need to take a physical action. This action is taken when any new data is published and the decision to publish data is taken on the microcontroller. The template that is used for this can be viewed below. It is just a modified discord template that Adafruit IO provides.
```
{
  "username": "{{feed_name}}",
  "content": "Your window is {{value}}! you should change that!"
}
```
The messages looks like this.
<img src="https://hackmd.io/_uploads/ByVzlitUA.png" 
    alt= Screenshot of discord messages>



## Presenting the data
Making a dashboard in Adafruit IO is very simple. You simply choose a feed and in what way you want to display the data.

I wanted the to group the humidity values and temperature values respectivly.
<img src="https://hackmd.io/_uploads/rkWExsKUA.png"
     alt="Screenshot of Adafruit dashboard" />


This way you can compare the values easier. The window state block is updated with the window feed that is used to trigger an action. The debug block functions like a summary for all data, this helped me to modify the decision in the code when an action is needed or not. It is also used as an alternative to the graphs. The gauge block also functions as an alternative to the graphs but only displays the most relative data for this project, the temperature indoors that we want to regulate. We also want to regulate humidity, however this is a secondary focus.

## Finalizing the design
The project went well and was fun to implement. As stated I would like to implement the TIG stack in place of Adafruit IO and with that make adjustments to the code, abstracting decision making of sending the webhook message to an external recource. 

The biggest hurdle of this project was to implement the logic of whether the window should be open or not, this was the subject of many git commits, however now I think it is good. More logic can also be implemented like when humidity is at a certain point in comparison to the temperature but I wanted to focus more on the temperature.

A fully automated solution could also be implemented, using some kind of actuator to physically open/close the window in place of the webhook telling me to do it. The logic is essentially there already, it would just require hooking up this actuator and adding the trigger to activate it in the same if statement where the data is published.
