# HallProbe

## Table of Contents

- [HallProbe](#hallprobe)
  - [Table of Contents](#table-of-contents)
  - [General Description](#general-description)
  - [🛠️ Hardware Requirements](#️-hardware-requirements)
  - [💻 Software Requirements](#-software-requirements)
  - [🔌 Wiring](#-wiring)
  - [📝 Code](#-code)
  - [💡 Remarks](#-remarks)
  - [⚙️ Register Configuration Details](#️-register-configuration-details)

## General Description

This application aims to drive the TMAG5273D2 sensor using I2C communication to measure temperature and magnetic fields along the X, Y, and Z axes.

## 🛠️ Hardware Requirements

- TMAG5273D2 sensor
- Arduino or compatible microcontroller
- I2C communication wires

## 💻 Software Requirements

- Arduino IDE
- Wire library (included with Arduino IDE)

## 🔌 Wiring

Connect the TMAG5273D2 sensor to the Arduino as follows:

- VCC to 3.3V or 5V
- GND to GND
- SDA to A4 (or the corresponding SDA pin on your board)
- SCL to A5 (or the corresponding SCL pin on your board)

For correct pullups of the different pins of the sensor it is recommended to replicate following circuit [Manual](https://docs.sparkfun.com/SparkFun_Qwiic_Hall_Effect_Sensor_TMAG5273/assets/board_files/schematic-mini.pdf).

## 📝 Code

Upload the `HallProbe.ino` sketch to your Arduino.

The value of the registers are taken from the document [tmag5273.pdf](tmag5273.pdf).

## 💡 Remarks

If the exact TMAG5273 version is not known, initial communication with the sensor can be set up by doing a sweep over all I2C addresses when the sensor is connected to a Arduino. (this will give from Table 6-2 in the [datasheet](tmag5273.pdf) the version (A,B,C or D)).
The sensor version can be determined `DEVICE_ID` register (0xdh), which indicates the sensitivity range (this gives information if it is a x1 or x2 sensor).

We tried to use the [Sparkfun Library](https://github.com/sparkfun/SparkFun_TMAG5273_Arduino_Library) for the TMAG, however it seems to be programmed a bit sloppy (we have seen copy paste errors in the library). Furthermore we are using the TMAG5273D2 while Sparkfun wrote their library for the a TMAG5273x1 while we are using the TMAG5273x2, such that we would have had to change sensitivity values in the library. Therefore we decided to set the registers "by hand" to the desired value.

## ⚙️ Register Configuration Details

1. **DEVICE_CONFIG_1 (0x00)**

   - Set to 0x14
   - Enables 32x measurement averaging (bits 4-2 = 101)
   - Uses standard I2C read mode

2. **DEVICE_CONFIG_2 (0x01)**

   - Set to 0x02
   - Configures device for continuous measurement mode

3. **SENSOR_CONFIG_1 (0x02)**

   - Set to 0x70
   - Bits 7-4 set to 7h (111) for sensor configuration
   - Enables X, Y, Z, and temperature channel measurements

4. **SENSOR_CONFIG_2 (0x03)**

   - Set to either 0x00 or 0x03 depending on MAGNETIC_RANGE
   - 0x00: Sets X_Y_RANGE=0 and Z_RANGE=0 for ±40 mT range which we used for higher sensitivity
   - 0x03: Sets X_Y_RANGE=1 and Z_RANGE=1 for ±80 mT range

The configuration provides:

- 32x averaging for noise reduction
- Continuous measurement mode for real-time monitoring
- Three-axis magnetic field measurements
- Configurable magnetic field range selection by selecting `MAGNETIC_RANGE` in the beginning of the code
