"""The file contains a collection of often used utility functions"""

import os
import sys
import shutil
import time
import logging
from typing import Tuple, Union

import numpy as np
import matplotlib.pyplot as plt


def report_time(t0: time.time, t1: time.time = None) -> None:
    """This function reports the delta between intial time point t0 and previous time point t1
    t0: Initial time point
    t1: Previous time point
    returns: current time
    """
    now = time.time()
    dt0 = now - t0
    if t1:
        dt1 = now - t1
        logging.info(
            """
Time since t0 : %s seconds
Time since previous = %s seconds
""",
            dt0,
            dt1,
        )
    else:
        logging.info("Time since t0 : %s seconds", dt0)
    return now


def fourier_transform(
    data: np.ndarray,
    n_samples: int,
    sampling_rate: Union[float, int],
    plot=False,
    label=None,
):
    """This function takes a time domain voltage data and returns the Fourier transform of the data

    Args:
        data: The time domain voltage data
        n_samples: The number of samples in the data
        sampling_rate: The sampling rate of the data
        plot: If True the function will plot the Fourier transform and return the figure
        label: The label of the plot

    Returns:
        The Fourier transform of the data
    """
    fft_result = np.fft.fft(data)
    frequencies = np.fft.fftfreq(n_samples, d=1 / sampling_rate)

    # FFT returns also negative frequencies, so we make them positive
    positive_frequencies = frequencies[frequencies > 0]
    positive_fft = abs(fft_result[frequencies > 0])

    data_stack = np.column_stack([positive_frequencies, positive_fft])

    fig = None
    if plot:
        fig = plot_fft(positive_fft, positive_frequencies, label=label)
    return data_stack, fig


def plot_fft(positive_fft, positive_frequencies, label=None):
    """Simple function for plotting a Fourier transform

    Args:
        positive_fft: The Fourier transform data
        positive_frequencies: The positive frequencies of the Fourier transform
        label: The label of the plot

    Returns:
        The figure object"""

    # Create the figure and axes
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Plot the FFT data
    ax.plot(positive_frequencies, positive_fft)

    # Set axis labels
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")

    # Set the y-axis to logarithmic scale
    ax.set_yscale("log")

    # Add a grid
    ax.grid(True)
    ax.set_title(label)

    # Return the figure object
    return fig


def plot_time_domain_voltage(
    time_domain_voltage: np.ndarray,
    times: Union[np.ndarray, None] = None,
    sampling_freq: Union[float, None] = None,
    duration: Union[float, None] = None,
    input_config: Union[object, None] = None,
    label: Union[str, None] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """Simple function for plotting the analog input

    Args:
        time_domain_voltage: The time domain voltage data
        times: The time axis
        sampling_freq: The sampling frequency
        duration: The duration of the signal
        input_config: The input configuration
        label: The label of the plot

    Returns:
        The figure object"""

    # Generate time axis using the sampling rate and buffer size
    if times is None:
        times = np.linspace(0, duration, num=duration * sampling_freq)

    # Create the figure and axes
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Plot the data
    ax.plot(
        times,
        time_domain_voltage,
        linewidth=0.04,
        marker="o",
        markersize=0.5,
        color="b",
    )

    # Set axis labels
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"Analog in channel {input_config.channel} (V)")
    ax.grid(True)
    ax.set_title(label)

    # Return the figure object
    return fig, ax


def initialize_logger(directory: str, label: str) -> None:
    """Sets up logging to both a file and the console.

    Args:
        directory: The directory to save the log file
        label: The label of the log file
    """
    # Create the results directory if it doesn't exist
    os.makedirs(f"{directory}/{label}", exist_ok=True)

    # Set up log file path
    log_file_path = f"{directory}/{label}/{label}.log"

    # Set up the logging configuration
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Adjust level as needed

    # Clear any existing handlers (to avoid duplicates if re-running the code)
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler (writes to log file)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)  # Log everything to the file
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (writes to console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # Set level for console output
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Example log message to confirm setup
    logger.info(
        "Logger initialized. All console output will also be written to the log file."
    )


def empty_directory(directory: str) -> None:
    """Removes all files and directories from the specified directory.

    Args:
        directory (str): The path to the directory to empty.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # Remove files and symbolic links
            elif os.path.isdir(file_path):
                shutil.rmtree(
                    file_path
                )  # Recursively remove directories and their contents
        # pylint: disable=broad-except
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def write_to_file(data_stack: np.ndarray, file_name: str) -> None:
    """This function take a data_stack and appends it to a specified csv file

    Args:
        data_stack: The data to write to the file
        file_name: The file to write the data to

    Returns:
        None
    """
    data_to_write = np.vstack(data_stack)
    with open(file_name, "a", encoding="UTF-8") as file:
        np.savetxt(file, X=data_to_write, delimiter=",", fmt="%.6f")


def prepare_directory(
    directory: str, label: str, clear_dir: bool = True, print_out: bool = True
) -> str:
    """Function that defines a directory path and creates or clears the directory
    
    Args:
        directory: The directory to create or clear
        label: The label of the directory
        clear_dir: If True the directory is cleared
        print_out: If True the function prints the actions taken
    
    Returns:
        The directory path"""
    dir_path = os.path.join(directory, label)
    os.makedirs(dir_path, exist_ok=True)
    if clear_dir:
        empty_directory(dir_path)
        if print_out:
            logging.info("The %s directory has been prepared and cleared", dir_path)
    else:
        if print_out:
            logging.info("The %s directory has been prepared and not cleared", dir_path)

    return dir_path


def pi_pulse(
    bandwidth: float = 100e3,
    b_0: float = 50e-3,
    duration: float = 1e-3,
    sampling_freq: float = 125e6,
    amplitude: float = 1,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a sinusoidal RF pulse with a given bandwidth, b_0, and Larmor frequency.
    Function is not used in the current implementation.
    But can be used to generate a pi pulse.
    Needs to be checked and tested. Bandwidth is not used in the current implementation.

    Args:
        bandwidth: The bandwidth of the RF pulse
        b_0: The strength of the magnetic field
        duration: The duration of the RF pulse
        sampling_freq: The sampling frequency
        amplitude: The amplitude of the RF pulse
    
    Returns:
        The time array and the RF pulse
    """
    # Calculate gamma (gyromagnetic ratio)
    gamma = 42.577478518e6
    center_freq = gamma * b_0 / (2 * np.pi)
    # duration = 0.44/bandwidth
    print(gamma, bandwidth)
    # Time array
    t = np.arange(0, duration, 1 / sampling_freq)

    t_center = duration / 2
    sigma = duration / (
        2 * np.sqrt(2 * np.log(2))
    )  # Standard deviation for FWHM = T --> checken
    envelope = np.exp(-((t - t_center) ** 2) / (2 * sigma**2))

    # Calculate the RF amplitude based on the Larmor frequency and bandwidth

    # print(b1_amplitude)
    # Generate the sinusoidal modulation at the Larmor frequency
    b1 = amplitude * envelope * np.sin(2 * np.pi * center_freq * t)

    return t, b1


def create_pi_pulses(
    data_dir: str,
    bandwidth: float=100e3,
    pi_duration: float=2e-3,
    sampling_freq: float=125e6,
    amplitdue: float=1,
) -> np.ndarray:
    """Function that creates a pi pulse and a half pi pulse and saves them to a csv file
    
    Args:
        data_dir: The directory to save the pi pulses
        bandwidth: The bandwidth of the RF pulse
        pi_duration: The duration of the RF pulse
        sampling_freq: The sampling frequency
        amplitude: The amplitude of the RF pulse
        
    Returns:
        The pi pulse stack"""
    t, b_pi = pi_pulse(
        duration=pi_duration,
        amplitude=amplitdue,
        sampling_freq=sampling_freq,
        bandwidth=bandwidth,
        b_0=50e-3,
    )
    t_2, b_half_pi = pi_pulse(
        duration=pi_duration / 2,
        amplitude=amplitdue,
        sampling_freq=sampling_freq,
        bandwidth=bandwidth,
        b_0=50e-3,
    )
    b_half_pi = np.interp(t, t_2, b_half_pi)
    pi_pulse_stack = np.column_stack([t, b_pi, b_half_pi])
    pi_header = "time (s), pi_pulse (V), half_pi_pulse (V)"
    np.savetxt(
        f"{data_dir}/pi_pulse.csv", X=pi_pulse_stack, delimiter=",", header=pi_header
    )

    plt.plot(t, b_pi, alpha=0.5, label="Pi pulse")
    plt.plot(t, b_half_pi, alpha=0.5, label="Half pi pulse")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.legend()
    plt.title("Pi pulses")
    plt.savefig(f"{data_dir}/pi_pulse.png")
    plt.xlim(0, t[5000])
    plt.savefig(f"{data_dir}/pi_pulse_zoomed.png")
    print(f"Saved png at: {data_dir}/pi_pulse.png")

    return pi_pulse_stack


def rgd_normalization(values):
    """Function that normalizes data between -1 and 1
    Args:
        values: The values to normalize
    Returns:
        The normalized values
    """
    return 2 * (values - min(values)) / (max(values) - min(values)) - 1


def report_max_mean_min(
    data_set: np.ndarray,
) -> Tuple[np.float64, np.float64, np.float64]:
    """Function that reports the max, mean and min of a data set
    
    Args:
        data_set: The data set to report the max, mean and min
        
    Returns:
        The mean, max and min of the data set"""
    mean_, max_, min_ = np.mean(np.abs(data_set)), np.max(data_set), np.min(data_set)
    logging.info("The mean of the absolute time domain voltage is: %s", mean_)
    logging.info("The max of the  time domain voltage is: %s", max_)
    logging.info("The min of the  time domain voltage is: %s", min_)
    return mean_, max_, min_


def windowed_rms(data: np.ndarray, window_size: int = 50) -> np.ndarray:
    """Calculate the windowed RMS of the data
    
    Args:
        data: The time domain voltage data
        window_size: The size of the window. Needs to be an even number
    
    Returns:
        The windowed RMS of the data"""
    rms = []
    for i in range(int(window_size / 2), data.shape[0] - int(window_size / 2)):
        rms.append(np.sqrt(np.mean(data[i : i + window_size] ** 2)))
    return np.array(rms)


def windowed_mean(data: np.ndarray, window_size: int = 50) -> np.ndarray:
    """Calculate the windowed RMS of the data
    
    Args:
        data: The time domain voltage data
        window_size: The size of the window. Needs to be an even number
    
    Returns:
        The windowed RMS of the data"""
    rms = []
    for i in range(int(window_size / 2), data.shape[0] - int(window_size / 2)):
        rms.append(np.mean(data[i : i + window_size]))
    return np.array(rms)


# Function that normalizes data with negative values
def normalize(data: np.ndarray) -> np.ndarray:
    """Normalize data with negative values
    
    Args:
        data: The data to normalize
        
    Returns:
        The normalized data"""
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def isolate_peak(data, discard=0.1, threshold=2e-2) -> Tuple[float, float]:
    """Removes first 0.1 seconds and the part of the signal where the signal below the threshold.
    Args:
        data: The time domain voltage data
        discard: The time to discard from the start of the signal
        threshold: The threshold value for the signal
    Returns:
        The start and end time of the peak
    """
    mask1 = (
        data[:, 0] > discard
    )  # Filters out the first 0.1 seconds wherin the signal is not stable
    mask2 = (
        data[:, 1] > threshold
    )  # Filter out the part of the signal where the signal is too small
    mask = mask1 & mask2
    filtered = data[mask]
    return filtered[0, 0], filtered[-1, 0]


def filter_peak(
    data: np.ndarray, t_start: float, t_end: float, buffer=0.1
) -> np.ndarray:
    """Filters the peak of the signal
    Args:
        data: The time domain voltage data
        t_start: The start time of the peak
        t_end: The end time of the peak
        buffer: The buffer time to add to the start and end time
    Returns:
        The filtered peak of the signal
    """
    mask1 = data[:, 0] > t_start - buffer
    mask2 = data[:, 0] < t_end + buffer
    mask = mask1 & mask2
    return data[mask]


def find_trailing_edge(
    data: np.ndarray, t_end_peak: float, t_range=0.00003
) -> np.ndarray:
    """Finds the trailing edge of the signal. The trailing edge is defined as the part of the signal
    that is below the buffer value.
    Args:
        data: The time domain voltage data
        t_end_peak: The end time of the peak
        t_range: The range of the trailing edge
    Returns:
        The trailing edge of the signal
    """
    mask1 = data[:, 0] > t_end_peak - t_range
    mask2 = data[:, 0] < t_end_peak + t_range
    mask = mask1 & mask2
    return data[mask]


def filter_out_edges_time_domain(
    time_domain_voltage: np.ndarray,
    buffer_size: float = 0.05,
    extra_buffer: float = 0.001,
) -> np.ndarray:
    """Filters the time domain voltage data by removing the edges of the signal
    Args:
        time_domain_voltage: The time domain voltage data
        buffer_size: The buffer size to remove the edges of the signal
        extra_buffer: Extra buffer to remove the edges of the signal

    Returns:
        The filtered time domain voltage
    """
    mask1 = (
        time_domain_voltage[:, 0]
        > time_domain_voltage[0, 0] + buffer_size + extra_buffer
    )
    mask2 = (
        time_domain_voltage[:, 0]
        < time_domain_voltage[-1, 0] - buffer_size - extra_buffer
    )
    mask = mask1 & mask2
    return time_domain_voltage[mask]


def prepare_all_directories(
    params: object,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> None:
    """Function that prepares all directories for the experiment

    Args:
        params: The parameters of the experiment
        frequency: The frequency of the experiment
        repeat: The repeat number of the experiment

    Returns:
        None
    """
    # Set the frequency, if not set use the default frequency
    if frequency is None:
        frequency = params.output.carrier.frequency

    params.output.carrier.frequency = frequency

    # Create the label for the measurement
    if repeat is None:
        params.mnt.label = f"{int(frequency/1000)}_kHz"
    else:
        params.mnt.label = f"{int(frequency/1000)}_kHz_{repeat+1}"

    params.run.data_dir = prepare_directory(
        f"data/{params.experiment}", params.run.label, clear_dir=False
    )

    params.run.analysis_dir = prepare_directory(
        f"analysis/{params.experiment}", params.run.label, clear_dir=False
    )

    params.run.result_dir = prepare_directory(
        f"results/{params.experiment}", params.run.label, clear_dir=False
    )

    params.mnt.data_dir = prepare_directory(
        params.run.data_dir, params.mnt.label, clear_dir=False
    )

    params.mnt.analysis_dir = prepare_directory(
        params.run.analysis_dir, params.mnt.label, clear_dir=False
    )

    params.mnt.result_dir = prepare_directory(
        params.run.result_dir, params.mnt.label, clear_dir=False
    )


def set_frequency_and_label(
    params: object,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> None:
    """Function that sets the frequency and label for the experiment

    Args:
        params: The parameters of the experiment
        frequency: The frequency of the experiment
        repeat: The repeat number of the experiment

    Returns:
        None
    """
    # Set the frequency, if not set use the default frequency
    if frequency is None:
        frequency = params.output.carrier.frequency

    params.output.carrier.frequency = frequency

    # Create the label for the measurement
    if repeat is None:
        params.mnt.label = f"{int(frequency/1000)}_kHz"
    else:
        params.mnt.label = f"{int(frequency/1000)}_kHz_{repeat+1}"
