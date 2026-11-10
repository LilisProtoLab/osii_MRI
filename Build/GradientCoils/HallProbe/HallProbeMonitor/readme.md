# HallProbeMonitor

## Table of Contents

- [HallProbeMonitor](#hallprobemonitor)
  - [Table of Contents](#table-of-contents)
  - [General Description](#general-description)
  - [System Requirements](#system-requirements)
  - [Main Features](#main-features)
    - [Terminal user interface and in-time plotting](#terminal-user-interface-and-in-time-plotting)
  - [How to Use](#how-to-use)

---

## General Description

This application is designed to monitor the data from the 3d hall probe using Python's IO port monitoring ability. 📊

## System Requirements

The code is written in `Python` and requires the following libraries:

- `CPython` Version `3.13.1`
- `Matplotlib` Version `3.10.0`
- `Numpy` Version `2.2.1`
- `Pyserial` Version `3.5`

You can use `pip` to install the required libraries or use a modern package manager like `uv` to install the libraries with `pyproject.toml`.

## Main Features

### Terminal user interface and in-time plotting

The program features a _user-unfriendly_ terminal interface that allows:

- **Output Magnetic Field**: Hall probe magnetic field data will be printed automatically in the terminal. 🧲
- **Export Data**: Magnetic data will be automatically saved in the `output.csv` in the same directory as the executable file. 💾

## How to Use

1. **Change serial port**: Change the serial port in code. 🔌
2. **Change Baud Rate**: Change the baud rate in code. ⚙️
3. **View Results**: Results will be printed in the terminal. 📜
4. **View Plot**: A window with real time plotting will be popped up to show the results. 📈
5. **Export Results**: Data will be automatically exported in the same directory of the program after you terminate the program. 📂
