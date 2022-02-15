## TinyML with ESP32 and MicroPython
Implementation of TinyML in pure (micro)Python on ESP32. The setup collects accelerometer & gyro data. Uses ML algorithm (Random Forest Classifier) to detect gestures from the collected (acceleration & gyro) time-series data. It detects 3 types of gestures:
  1. Movement along X axis
  2. Movement along Y axis
  3. Circle Movement

It sends the collected data and detected gestures to backend that saves data into a database.

Blog: [TinyML: Machine Learning on ESP32 with MicroPython](https://dev.to/tkeyo/tinyml-machine-learning-on-esp32-with-micropython-38a6)

## MicroPython
- v 1.14 for ESP32 ([download](https://micropython.org/download/esp32/))

## Bill of materials

- ESP32-devkitC
- MPU6500
- breadboard
- jumper wires

## Schema

**Pin details**

SCL = pin 22

SDA = pin 21


![image](https://user-images.githubusercontent.com/47578763/154149241-2f44bd96-1dfe-452b-90a2-aa16dc9b7d36.png)

## Setup
1. Check the port. On MacOS use `ls /dev/cu.*`. Linux, Windows and more info on establishing connection on this site [Espressif - Establish Serial Connection with ESP32](-idf/en/latest/esp32/get-started/establish-serial-connection.html#)
2. Flash the ESP32 - Follow **Installation instructions** here [ESP32](https://micropython.org/download/esp32/)
3. For convenience use Pymakr VSCode extension [Pymakr VSCode](https://docs.pycom.io/gettingstarted/software/vscode/)
4. Upload Python scripts to ESP32 using Pymakr Extension
