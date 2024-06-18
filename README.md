# Smart Climate Control System For A Window

[![hackmd-github-sync-badge](https://hackmd.io/ZVxbMHrCR8-jHQ3t1b0l-g/badge)](https://hackmd.io/ZVxbMHrCR8-jHQ3t1b0l-g)


    Author: Gustaf Nordlander (gn222ia)
**Overview:** This tutorial will show you how to make a smart climate control system in the form of a system that measures values outdoors and indoors. The system notifies that an action needs to be taken, the window it is attached to needs to close or open to effectivly regulate the climate indoors.

Expect around - hours

## Objective
During the summer it can be difficult regulating temperature inside your home. Energy consumtion can increase with the use of fans or AC's. A simple way to help lower the use of these potentially powerhungry electronics is to open your window when it is colder outside and close it when it is hotter. For some however it can be difficult to remember to do this and to make a habit  of it. 

## Materials
The components used in this project were bought from [Electrokit](https://www.electrokit.com/).

|Picture| Component | Description | Price (SEK) |
|---------| --------- | ----------- | ----------- |
|href| Text      | Text        | Text        |
|href| Text      | Text        | Text        |
|href| Text      | Text        | Text        |
|href| Text      | Text        | Text     |

The Pico WH microcontroller used is a good starting point for a IoT project if you have no prior experience with building an IoT device in my opinion. It has wifi capabilities so many simple projects that you might want to make in your apartment are possible.



## Computer Setup
### Flash the firmware
To operate the microcontroller you will need the micropython firmware.
Follow these steps to flash the firmware onto your Pico WH:
1. Download the micropython firmware which you will find [here.](https://www.micropython.org/download/RPI_PICO_W/)
2. While holding down the BOOTSEL button on the Pico WH plug it in to your computer.
3. You should now see the microcontroller as a USB drive on the computer.
4. Simply drag the firmware file to the USB drive to copy it onto the Pico WH.
The USB drive should now dissapear wich means the process was successfully done.
### IDE
Visual Studio Code was my choice of IDE to program the Pico WH microcontroller due to prior experience with the IDE. It has a large community that supports it with many different plugins making it a diverse IDE.

1. Install [Visual Studio Code](https://code.visualstudio.com/). Click the arrow next to the download button for download links to more operating systems.
2. 

The plugin you need for this project is pymakr.
