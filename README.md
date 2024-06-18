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
