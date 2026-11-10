"""File containing the analysis of the free spin decay experiment"""

import os
import sys
from typing import Union, Tuple

import numpy as np
import matplotlib.pyplot as plt

# If the sourc directory is not in the sys.path, add it
source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if source_dir not in sys.path:
    sys.path.append(source_dir)
    sys.path.append(os.path.join(source_dir, "src"))

# pylint: disable=wrong-import-position
from src.utils import set_frequency_and_label, windowed_mean, normalize, prepare_all_directories
from config import free_spin_decay as config

plt.style.use("seaborn-v0_8")

# Null format for plots
null_format = {"color": "orange", "label": "Null", "alpha": 0.7}

# Sample format for plots
sample_format = {"color": "purple", "label": "Sample", "alpha": 0.7}

COLOR_GREEN = "#8DC353"
COLOR_BLUE = "#1C458A"


def run(
    params: config.Parameters,
    data=None,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> Tuple[float, float]:
    """
    Run the analysis of the free spin decay experiment

    Args:
        params: The parameters of the experiment
        data: The time domain voltage data of the signal. If None the data is loaded from file
        frequency: The frequency of the experiment if None the default frequency is used
        repeat: The repeat number of the experiment if None no repeat is used

    Returns:
        The decay time and the frequency of the signal
    """

    # Set the frequency, if not set use the default frequency
    set_frequency_and_label(params, frequency, repeat)

    print(params.mnt.label)

    # Prepare the directories
    prepare_all_directories(params, frequency, repeat)

    if data is None:
        # If there is no file return None
        if not os.path.isfile(
            f"{params.mnt.data_dir}/decay_time_domain_voltage.csv"
        ):
            print(
                f"{params.mnt.data_dir}/decay_time_domain_voltage.csv does not exist. Skipping...\n"
            )
            return None
        time_domain_voltage = np.loadtxt(
            f"{params.mnt.data_dir}/decay_time_domain_voltage.csv",
            delimiter=",",
        )
    else:
        time_domain_voltage = data

    # Take the absolute value of the voltage
    time_domain_voltage = np.abs(time_domain_voltage)

    # Plot the signal
    plt.figure()
    plt.plot(time_domain_voltage[:, 0], time_domain_voltage[:, 2])
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title(f"Signal: {params.mnt.label}")
    plt.savefig(f"{params.mnt.analysis_dir}_signal.png")
    plt.close()

    # Create subplots

    _, axs = plt.subplots(2, 2, figsize=(10, 8))

    times = time_domain_voltage[:, 0] - min(time_domain_voltage[:, 0])

    # Quick plot
    axs[0, 0].plot(times * 1000, time_domain_voltage[:, 1], **null_format)
    axs[0, 0].set_xlabel("Time (ms)")
    axs[0, 0].set_ylabel("Voltage (V)")
    axs[0, 0].set_title("Voltage vs Time")
    axs[0, 0].legend()

    # Slide a window over the time domain voltage and calculate the RMS

    params.proc.window_size = 16

    rms_voltage = windowed_mean(
        time_domain_voltage, window_size=params.proc.window_size
    )

    rms_times = (
        times[int(params.proc.window_size / 2) : int(-params.proc.window_size / 2)]
        + params.proc.window_size / params.input.sampling_rate
    )

    # Plot RMS voltages
    axs[0, 1].plot(rms_times * 1000, rms_voltage, **null_format)
    axs[0, 1].set_xlabel("Time (ms)")
    axs[0, 1].set_ylabel("Mean Voltage (V)")
    axs[0, 1].legend()
    axs[0, 1].set_title("Sliding window mean Voltage vs Time")

    # Calculate the change in RMS voltage
    delta_rms_voltage = np.diff(rms_voltage, n=1)

    # Ajust the time array to match the length of the change in RMS voltage
    delta_rms_times = (
        rms_times[: delta_rms_voltage.shape[0]] + 1 / params.input.sampling_rate
    )

    # Plot change in RMS voltages
    axs[1, 0].plot(
        times[: delta_rms_voltage.shape[0]] * 1000,
        delta_rms_voltage * 1000,
        **null_format,
    )
    axs[1, 0].set_xlabel("Time (ms)")
    axs[1, 0].set_ylabel("Change in mean Voltage (V/s)")
    axs[1, 0].legend()
    axs[1, 0].set_title("Change in mean Voltage vs Time")

    # Slide a window over the change in RMS voltage and calculate the mean
    params.proc.window_size = 50

    mean_delta_rms_voltage = windowed_mean(
        delta_rms_voltage, window_size=params.proc.window_size
    )

    start_index = int(params.proc.window_size / 2)
    end_index = int(-params.proc.window_size / 2)

    mean_delta_rms_times: np.ndarray = (
        delta_rms_times[start_index:end_index]
        + params.proc.window_size / params.input.sampling_rate
    )

    # Find the last index where the value of the mean change in
    # RMS voltage is below the threshold
    threshold = np.mean(mean_delta_rms_voltage) - 0.2 * np.abs(
        np.mean(mean_delta_rms_voltage)
    )

    # Find the times where the mean change in RMS voltage is below the threshold
    times_below_threshold = mean_delta_rms_times[mean_delta_rms_voltage < threshold]

    # Find the first and last time values where the mean change
    # in RMS voltage is below the threshold
    t_last = times_below_threshold[-1]

    t_first = times_below_threshold[0]

    # Calculate the time difference between the minimum
    #  and the last index
    decay_time = t_last - t_first

    # Plot change in RMS voltages
    axs[1, 1].plot(
        mean_delta_rms_times * 1000,
        mean_delta_rms_voltage,
        **null_format,
    )

    axs[1, 1].axvline(t_first * 1000, color="red", linestyle="--")
    axs[1, 1].axvline(t_last * 1000, color="red", linestyle="--")
    axs[1, 1].axhline(threshold, color="green", linestyle="--")
    axs[1, 1].set_xlabel("Time (s)")
    axs[1, 1].set_ylabel("Change in mean Voltage (V)")
    axs[1, 1].legend()
    axs[1, 1].set_title("Sliding window mean change in Voltage vs Time")

    # plt.suptitle(f"Frequency: {params.mnt.label}")
    plt.tight_layout()
    plt.savefig(f"{params.mnt.analysis_dir}_rms_voltage.png")
    plt.close()

    # Plot the RMS voltages vs time and the windowed change in RMS voltage
    plt.figure()
    plt.plot(
        rms_times * 1000,
        normalize(rms_voltage),
        label="Null",
        alpha=0.5,
    )
    plt.plot(
        mean_delta_rms_times * 1000,
        normalize(mean_delta_rms_voltage),
        label="Null mean change",
        alpha=0.5,
    )
    plt.axvline(
        t_first * 1000,
        color="red",
        linestyle="--",
        label="Min Null",
        alpha=0.5,
    )
    plt.axvline(
        t_last * 1000,
        color="red",
        linestyle="--",
        label="Last Null",
        alpha=0.5,
    )
    plt.xlabel("Time (ms)")
    plt.ylabel("RMS Voltage (V)")
    plt.legend()
    plt.title(f"RMS Voltage vs Time: {params.mnt.label}")
    plt.savefig(f"{params.mnt.analysis_dir}_rms_change_voltage.png")
    plt.close()
    # Report the results
    print(f"Decay time of the null signal: {decay_time}")

    # Slice the data so only to look at the decay
    time_domain_voltage = time_domain_voltage[
        int(t_first * params.input.sampling_rate) : int(
            t_last * params.input.sampling_rate
        )
    ]

    # Take the FFT of the time domain voltage
    freq_domain_voltage = np.fft.fft(time_domain_voltage[:, 1])
    frequencies = np.fft.fftfreq(
        time_domain_voltage[:, 1].shape[0], 1 / params.input.sampling_rate
    )

    # Plot the frequency domain voltage
    plt.figure()
    plt.plot(
        frequencies,
        np.abs(freq_domain_voltage),
        **null_format,
    )

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title(f"Frequency domain voltage: {params.mnt.label}")
    plt.legend()
    plt.savefig(f"{params.mnt.analysis_dir}_frequency_domain_voltage.png")
    plt.close()

    # Find the frequency of the signal of the frequencies highet than 1MHz
    slice_freq_domain_voltage = freq_domain_voltage[frequencies > 1e6]
    max_index = np.argmax(np.abs(slice_freq_domain_voltage))
    signal_frequency = frequencies[max_index]

    # Report the results
    print(f"Signal frequency: {signal_frequency}")

    # Save the results
    with open(
        f"{params.mnt.analysis_dir}/results.txt",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(f"Decay time of the null signal: {decay_time}\n")
        file.write(f"Signal frequency: {signal_frequency}\n")
    return decay_time, signal_frequency


if __name__ == "__main__":

    parameters = config.Parameters()
    example_data_path = "data/free_spin_decay/null/2128_kHz/decay_time_domain_voltage.csv"  # Add the path to the example data

    with open(example_data_path, "r", encoding="utf-8") as example_data_file:
        example_data = np.loadtxt(example_data_file, delimiter=",", encoding="utf-8")

    example_decay_time, example_signal_frequency = run(parameters, data=example_data)
    print(f"Decay time: {example_decay_time}")
    print(f"Signal frequency: {example_signal_frequency}")
