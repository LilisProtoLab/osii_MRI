# Configuration File for the Waveform Wizards

This repository contains the configuration files used for controlling and configuring the Waveform Wizards system. The system is designed to interface with the Analog Discovery Pro device to generate, modulate, and measure waveforms for various experiments.

## File Overview

The configuration files define several classes that encapsulate standard configurations for different aspects of the waveform generation and data acquisition process. Each class represents a component of the system and its parameters, making the code modular and easily adaptable.

---

## Configuration Files

### 1. **spin_echo.py**

Contains the configuration for the spin echo experiment.

### 2. **free_spin_decay.py**

Contains the configuration for the free spin decay experiment.

### 3. **copy_me.py**

Contains a template configuration that can be copied and modified for new experiments.

### 4. **paramagnetic.py**

Contains the configuration for the paramagnetic resonance experiment.

---

## Classes and Their Configurations

### 1. **Pi_pulse**

Represents the configuration for a standard pi-pulse in the waveform system.

- **Attributes:**
  - `bandwidth`: Bandwidth of the pulse (100 kHz).
  - `duration`: Duration of the pi pulse (1 ms).
  - `gamma`: Gyromagnetic ratio (42.577478518 Hz/T).
  - `wait_time`: Time between the pi pulse and half-pi pulse (5 ms).
  - `b_0`: Magnetic field strength (0.05 T).

- **Properties:**
  - `center_freq`: Center frequency or Larmor frequency (calculated from `b_0` and `gamma`).

---

### 2. **Carrier**

Represents the carrier wave configuration.

- **Attributes:**
  - `node`: The identifier for the signal node (default: 0).
  - `enable`: Boolean to enable or disable the carrier wave.
  - `channel`: Output channel for the carrier wave.
  - `function`: Waveform type (default: sine).
  - `frequency`: Carrier frequency (2.128 MHz).
  - `phase`: Phase in radians (default: 0).
  - `amplitude`: Signal amplitude (5 V).
  - `offset`: Offset voltage (0 V).
  - `symmetry`: Symmetry percentage (default: 50%).

---

### 3. **FrequencyModulation**

Represents the configuration for frequency modulation.

- **Attributes:**
  - `enable`: Boolean to enable or disable frequency modulation.
  - `node`: Identifier for the signal node (default: 1).
  - `channel`: Output channel for the FM signal.
  - `function`: Waveform type (default: ramp up).
  - `frequency`: Modulation frequency.
  - `phase`: Phase in radians (default: 0).
  - `amplitude`: Modulation amplitude (0 - 100).
  - `offset`: Offset voltage (20 V).

---

### 4. **AmplitudeModulation**

Represents the configuration for amplitude modulation.

- **Attributes:**
  - `enable`: Boolean to enable or disable amplitude modulation.
  - `node`: Identifier for the signal node (default: 2).
  - `channel`: Output channel for the AM signal.
  - `function`: Waveform type (default: ramp up).
  - `frequency`: Modulation frequency (1 Hz).
  - `phase`: Phase in radians (default: 0).
  - `amplitude`: Modulation amplitude (5 mV).
  - `offset`: Offset voltage (0 V).

---

### 5. **OutputChannel**

Combines the carrier wave, amplitude modulation, and frequency modulation into a single output channel.

- **Attributes:**
  - `channel`: Output channel number (default: 1).
  - `carrier`: Instance of the `Carrier` class.
  - `am`: Instance of the `AmplitudeModulation` class.
  - `fm`: Instance of the `FrequencyModulation` class.
  - `enable`: Boolean to enable or disable the output signal.
  - `buffer_size`: Size of the output buffer (default: 32,768 samples).
  - `sampling_rate`: Sampling rate of the signal (125 MHz).
  - `run_time`: Duration the output signal is active (2 s).
  - `wait_time`: Delay before signal activation after a trigger (0 s).
  - `repeat`: Number of signal repetitions (default: 1).
  - `data`: Placeholder for storing output signal data.

---

### 6. **InputChannel**

Defines the configuration for the input channel.

- **Attributes:**
  - `buffer_size`: Size of the internal buffer (default: 134,217,728 samples).
  - `sampling_rate`: Sampling rate for data acquisition (10 MHz).
  - `channel`: Input channel number (0 for Channel 1, 1 for Channel 2).
  - `volts_range`: Maximum voltage range (±5 V).
  - `enable`: Boolean to enable or disable the input channel.

---

### 7. **Measurement**

Configuration for data acquisition measurements.

- **Attributes:**
  - `stabilization_time`: Time to wait for stabilization of the output channel (default: `0` seconds).
  - `buffer_time`: Buffer time between operations (default: `0.5` seconds).
  - `t_pre_signal`: Delay between pulse and data acquisition.
  - `duration`: Duration of data acquisition (23 ms).
  - `bit_mask_output`: Bitmask for output pins (default: `0b00000001`).
  - `bit_mask_s0`: Bitmask for off state (default: `0b00000000`).
  - `bit_mask_s1`: Bitmask for on state (default: `0b00000001`).
  - `data_dir`: Directory for storing raw data of a single measurement.
  - `result_dir`: Directory for storing results of a single measurement.
  - `label`: Measurement label.

---

### 8. **Run**

Defines the configuration for a measurement run.

- **Attributes:**
  - `resolution`: Number of measurements within the bandwidth (default: 1).
  - `time_between_mnt`: Time between consecutive measurements (1 s).
  - `mnt_repeats`: Number of repetitions per measurement (default: 10).
  - `label`: Label for the run (default: `'give_me_a_label'`).
  - `data_dir`: Directory for data storage.
  - `result_dir`: Directory for results.
  - `description`: Description of the run.

---

### 9. **Dwf**

Configuration for the Digilent Waveforms Framework.

- **Attributes:**
  - `device`: Device index (default: 0, the first detected device).
  - `config`: Configuration number for the AD Pro device.

---

### 10. **Processing**

Configuration for data processing.

- **Attributes:**
  - `epsilon`: Minimum accepted value in the data (2 µV).
  - `time_domain_zoom`: Time limits for zoomed plots in seconds (default: `(0.65, 0.7)`).
  - `save_data`: Boolean to enable or disable data saving.

---

### 11. **Parameters**

Encapsulates all configurations into a single interface for a measurement run.

- **Attributes:**
  - `pulse`: Instance of the `Pi_pulse` class.
  - `output`: Instance of the `OutputChannel` class.
  - `input`: Instance of the `InputChannel` class.
  - `run`: Instance of the `Run` class.
  - `dwf`: Instance of the `Dwf` class.
  - `proc`: Instance of the `Processing` class.
  - `mnt`: Instance of the `Measurement` class.

---

## Usage

1. **Import the Configuration**  
   Add the desired configuration file to your project and import the classes as needed.

   ```python
   from config.spin_echo import Parameters
   params = Parameters()
   ```

2. **Customize Parameters**

   ```python
   # Set new carrier frequency
   params.output.carrier.frequency = 2.5e6
   ```
