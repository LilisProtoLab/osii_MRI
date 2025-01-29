# HallProbe

## Table of Contents

- [HallProbe](#hallprobe)
  - [Table of Contents](#table-of-contents)
  - [General Description](#general-description)
  - [Usage](#usage)

## General Description

This subdirectory includes two projects: [HallProbeDriver](HallProbeDriver/) and [HallProbeMonitor](HallProbeMonitor/). The HallProbeDriver aims to drive the TMAG5273D2 sensor using I2C communication to measure temperature and magnetic fields along the X, Y, and Z axes. The HallProbeMonitor aims to monitor the data from the sensor and write the data into a csv file.

![HallProbe Setup](../Images/HallProbe.jpg)
(on the image the black wire is GND, red is 3.3V, white is SCL and red is SDA). The circuit on the board with the TMAG5273 is described in the `HallProbeDriver` folder

## Usage

1. 🖥️ Open the Arduino IDE.
2. 🔌 Connect your Arduino to your computer.
3. 📥 Upload the [sketch](HallProbeDriver/HallProbe/) to your Arduino.
4. 🖨️ Open the Serial Monitor to view the temperature and magnetic field measurements.
   For also saving the data:
5. 🐍 Open the [python](HallProbeMonitor/monitor.py)
6. ⚙️ Adjust the COM port in the beginning of the script (you can see the COM port of the Arduino in the Arduino IDE)
7. ▶️ Run the python script (measurements will be printed in terminal and a window with real time plotting will be popped up to show the results)
8. 💾 Data will be automatically saved in a .csv file called `output.csv` in the same directory of the program after you terminate the program
