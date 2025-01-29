"""Config file for the waveform wizards"""

import os
import sys
import numpy as np
from dataclasses import dataclass
from ctypes import c_ubyte


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# pylint: disable=wrong-import-position
from src._dwf.functions import Function


@dataclass
class PiPulse:
    """Standard configuration of the pi pulse"""

    def __init__(self):
        self.bandwidth = 100e3
        self.duration = 2e-3
        self.gamma = 42.577478518e6  # Hz/T Gyromagnetic ratio
        self.wait_time = 0.5e-2  # Time between the pi/2 and pi pulse
        self.b_0 = 5e-3  # T Magnetic field strength

    @property
    def center_freq(self):
        """Calculate the center frequency of the pulse"""
        return self.gamma * self.b_0 / (2 * np.pi)


class Carrier:
    """Standard configuration of the carrier wave"""

    def __init__(self):
        self.node = 0
        self.enable: bool = True
        self.channel = None
        self.function: c_ubyte = Function.sine
        self.frequency: float = (
            2.128e6  # Hz should be set to the center frequency of the pulse
        )
        self.phase: float = 0.0  # Radians
        self.amplitude: float = 5e-3  # V
        self.offset: float = 0  # Offset of the signal
        self.symmetry: float = 50

    @property
    def channel(self):
        """Getter for the channel attribute"""
        return self._channel

    @channel.setter
    def channel(self, value):
        """Setter for the channel attribute"""
        self._channel = value


class FrequencyModulation:
    """Standard configuration of the parameters the Frequency Modulation"""

    def __init__(self):
        self.enable: bool = False
        self.node = 1
        self.channel = None
        self.function: int = 4  # Ramp up
        self.frequency: float = None
        self.phase: float = 0
        self.amplitude = 100
        self.offset: float = 20  # Offset of the signal

    @property
    def channel(self):
        """Getter for the channel attribute"""
        return self._channel

    @channel.setter
    def channel(self, value):
        """Setter for the channel attribute"""
        self._channel = value


class AmplitudeModulation:
    """Standard configuration of the parameters the Amplitude Modulation"""

    def __init__(self):
        self.enable: bool = False
        self.node = 2
        self.channel = None
        self.function: int = 4
        self.frequency: float = 1
        self.phase: float = 0
        self.amplitude = 5e-3
        self.offset: float = 0  # Offset of the signal

    @property
    def channel(self):
        """Getter for the channel attribute"""
        return self._channel

    @channel.setter
    def channel(self, value):
        """Setter for the channel attribute"""
        self._channel = value


@dataclass
class OutputChannel:
    """Standard configuration of the parameters defining the morphology of
    the signal through the output channel for the AD2"""

    def __init__(self):
        self.channel: int = 1
        # The output channel is build up with the carrier wave,
        # amplitude modulation and frequency modulation nodes.
        self.carrier = Carrier()
        self.am = AmplitudeModulation()
        self.fm = FrequencyModulation()

        # Additional parameters
        self.enable: bool = True  # Start the signal
        self.buffer_size: int = (
            32768  # Size of the output buffer.
            # Standard the maximum size of the Anolog Discovery Pro
        )
        self.sampling_rate: int = (
            125e6  # The sampling rate of the output signal.
            # Standard the maximum sampling rate of the Anolog Discovery Pro
        )
        self.run_time: float = 2  # The time the output signal is active
        self.wait_time = 0  # The time the output signal is inactive after activation
        self.repeat = 1  # The number of times the output signal is repeated.
        # 1 means the signal is only send once.
        self.data = None  # Can be used to store the output signal

    def __post_init__(self):
        # Set the channel attribute in AM and FM based on channel_out
        self.carrier.channel = self.channel
        self.am.channel = self.channel
        self.fm.channel = self.channel


@dataclass
class InputChannel:
    """Standard configuration of the input channel for the AD2"""

    def __init__(self):
        self.buffer_size: int = (
            134217728  # Size of the internal buffer. Standard the maximum AD_Pro
        )
        self.sampling_rate: float = (
            10e6  # Hz. Arbitrary value may be to high.
        ) # At least two time the center frequency of the pulse
        self.channel: int = 0  #  0 --> Channel 1, 1 --> Channel 2
        self.volts_range: float = 5  # Maximum accepted voltage +-
        self.enable: bool = True


@dataclass
class Measurement:
    """Stand configuration of the measurements"""

    def __init__(self):
        self.t_pre_signal = (
            None  # The delay between data acquisition and the sending of the pulse
        )
        self.duration = 20e-3  # The duration of the data acquisition.
        self.bit_mask_output = int(
            0b00000001
        )  # Bit mask used to assigne which are the output pins
        self.bit_mask_s0 = int(0b00000000)  # Bit mask for the off state
        self.bit_mask_s1 = int(0b00000001)  # Bit mask for the on state
        self.data_dir = None  # Directory to store the data
        self.result_dir = None  # Directory to store the results
        self.label = None  # Label of the measurement
        self.frequency = None  # Used to store the frequency of the carrier wave
        self.repeat = (
            None  # Used to store the number of repeats of the measurement in a run
        )


@dataclass
class Run:
    """Stand configuration of the run"""

    def __init__(self):
        self.resolution = 5  # Number of different measurements in the bandwith
        self.time_between_mnt = 1  # Time between different measurements
        self.mnt_repeats = 3  # Number of times a measurement is repeated
        self.label = "fake"  # Label of measurement run
        self.data_dir = None
        self.result_dir = None
        self.analysis_dir = None
        self.desription = None


@dataclass
class Dwf:
    """Standard configuration of the Digilent Waveforms Framework"""

    def __init__(self):
        self.device = 0  # Take the first detected device
        self.config = 5  # Configuration number, see log files for the AD_Pro configuration options


@dataclass
class Processing:
    """Standard configuration of the data processing"""

    def __init__(self):
        self.epsilon = 2e-6  # Minimum accepted value in data.
        # Used to filter padded zero's in data. (Two times the stepsize of the AD Pro)
        self.time_domain_zoom = (0.65, 0.7)  # Time limit for zoomed plots in seconds
        self.save_data = True


@dataclass
class Parameters:
    """Standard configuration of the parameters detirmining the behaviour of the measurement run"""

    def __init__(self):
        self.experiment = "spin_echo"
        self.pulse = PiPulse()
        self.output = OutputChannel()
        self.input = InputChannel()
        self.run = Run()
        self.dwf = Dwf()
        self.proc = Processing()
        self.mnt = Measurement()
