# _dwf Directory

The `_dwf` directory contains modules and constants related to the Digilent WaveForms SDK, which is used for controlling Digilent devices such as the Analog Discovery 2 (AD2). This directory includes essential components for waveform generation, data acquisition, and device configuration.

## Structure

- **`__init__.py`**: This file contains the `load_dwfconstants` function, which dynamically loads the DWF constants based on the operating system.
- **`dwfconstants.py`**: This file defines various constants used by the DWF library, including device handles, enumeration filters, device IDs, trigger sources, instrument states, and analog out signal types.
- **`functions.py`**: This file defines a class that maps custom function names to the corresponding DWF constants.

## Purpose

The code in this directory is designed to:

1. **Load DWF Constants**: Dynamically load the appropriate DWF constants based on the operating system.
2. **Define DWF Constants**: Provide a comprehensive list of constants used by the DWF library for device control and configuration.
3. **Map Custom Function Names**: Define custom function names for easier reference in waveform generation and data acquisition scripts.

## How to Use

1. **Loading and using DWF Constants**:
   - Use the `load_dwfconstants` function from `__init__.py` to dynamically load the DWF constants based on your operating system.

   ```python
   from _dwf import load_dwfconstants
   constants = load_dwfconstants()
   sine = constants.funcSine

2. **Using Custom Function Names**:

    - Import the `functions` module to custom fuction names for waveform generation

    ```python
    from _dwf.functions import function

    sine = function.sine
