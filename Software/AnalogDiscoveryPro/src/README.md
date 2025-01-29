# Source Directory for WaveGen Project

This directory contains the source code for the WaveGen project, which is responsible for the waveform generation and data acquisition using the Digilent Analog Discovery 2 (AD2) device.

## Structure

- **`_dwf/`**: Contains modules and constants related to the Digilent WaveForms SDK.
  - **`__init__.py`**: Dynamically loads the DWF constants based on the operating system.
  - **`dwfconstants.py`**: Defines various constants used by the DWF library.
  - **`functions.py`**: Maps custom function names to the corresponding DWF constants.
  - **`utils.py`**: Contains utility functions relating to the Digilent devices
  - **`example_scripts/`**: Contains example scripts from the DWF frame work

- **`spin_echo/`**: Contains scripts related to spin echo experiments.
  - **`measurement.py`**: Script to run spin echo measurements.
  - **`processing.py`**: Script to run the processing of the data taken from the measurement
  - **`analysis.py`**: Script to run spin echo analysis on the processed data.
  - **`run.py`**: Main script to execute the entire workflow for spin echo experiments.
- **`free_spin_decay/`**: Contains scripts related to free spin decay experiments.
  - **`measurement.py`**: Script to run free spin decay measurements.
  - **`processing.py`**: Script to run the processing of the data taken from the measurement
  - **`analysis.py`**: Script to run free spin decay analysis on the processed data.
  - **`run.py`**: Main script to execute the entire workflow for waveform generation and data acquisition.
- **`paramagnetic/`**: Contains scripts related to free spin decay experiments.
  - **`measurement.py`**: Script to run free spin decay measurements. Need to adapt old script
  - **`processing.py`**: Script to run the processing of the data taken from the measurement
  - **`analysis.py`**: Script to run free spin decay analysis on the processed data.
  - **`run.py`**: Main script to execute the entire workflow for waveform generation and data acquisition.
- **`utils.py`**: Contains utility functions used across the project.

## Purpose

The code in this directory is designed to:

1. **Facilitate Waveform Generation**: Implement the logic for generating and acquiring waveform signals through the AD2 device.
2. **Process Data**: Handle the data collected during experiments, including filtering, transformation, and visualization.
3. **Support Experiment Reproducibility**: Enable consistent experimental conditions through configurable parameters.

## How to Use

1. **Initiate Data Acquisition**:

- Run the appropriate `run.py` script in the relevant directory (e.g., `spin_echo/run.py`, `free_spin_decay/run.py`, `paramagnetic/run.py`) to start the data acquisition process.

2. **Customize Experimental Settings**:

  - Modify the `config.py` file to set up your experimental parameters before running the main script.

3. **Utilize Utility Functions**:

  - Use the functions provided in `utils.py` for additional data handling and analysis tasks.

4. **Execute Workflow Scripts**:

- For specific experiments, run the corresponding `run.py` script in the relevant directory (e.g., `spin_echo/run.py`, `free_spin_decay/run.py`, `paramagnetic/run.py`) to execute the entire workflow.

5. **Analyze and Process Data**:

- Use the `measurement.py`, `processing.py`, and `analysis.py` scripts in the respective directories to measure, process, and analyze the experimental data.
- Use the functions in `utils.py` for additional data handling and analysis tasks.

## Analog Out Signal Types

In the function that outputs the carrier wave, with as option FM and AM, the functions that can be applied to the carrier, FM or AM wave are

- 0: DC
- 1: Sine
- 2: Square
- 3: Triangle
- 4: Ramp up
- 5: Ramp down
- 6: Noise
- 30: Custum wave
- 31: Play (audio file)

These values are passed to `output_config.function`, which sets the different waveforms





