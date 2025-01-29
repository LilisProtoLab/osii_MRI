"""File containing the analysis of the free spin decay experiment"""

import os
import sys
from typing import Union
import logging

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# If the sourc directory is not in the sys.path, add it
source_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
if source_dir not in sys.path:
    sys.path.append(source_dir)
    sys.path.append(os.path.join(source_dir, "src"))

# pylint: disable=wrong-import-position
from src.utils import (
    set_frequency_and_label,
    fourier_transform,
    windowed_rms,
    prepare_all_directories,
    initialize_logger,
)
from config import spin_echo as config

plt.style.use("seaborn-v0_8")

COLOR_GREEN = "#8DC353"
COLOR_BLUE = "#1C458A"


def run(
    params: config.Parameters,
    time_domain_voltage: Union[np.ndarray, None] = None,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> None:
    """
    Run the analysis of the free spin decay experiment

    Args:
        params: The parameters of the experiment
        time_domain_voltage: The time domain voltage data of the signal. If None the data is loaded from file
        frequency: The frequency of the experiment if None the default frequency is used
        repeat: The repeat number of the experiment if None no repeat is used

    Returns:
        None
    """

    # Set the frequency, if not set use the default frequency
    set_frequency_and_label(params, frequency, repeat)
    # Prepare the directories
    prepare_all_directories(params, frequency, repeat)
    initialize_logger("results", params.run.label)
    #Suppres matplotlib logging
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    # Load the data
    if time_domain_voltage is None:
        time_domain_voltage = np.loadtxt(
            f"{params.mnt.params.mnt.data_dir}/time_domain_voltage.csv", delimiter=","
        )

    # Plot the data with good style
    fig, ax = plt.subplots()
    ax.plot(
        time_domain_voltage[:, 0] / 1000, time_domain_voltage[:, 1], color="#8DC353"
    )
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage (V)")
    ax.grid(True)
    ax.set_title("Generated Spin Echo Data")
    fig.savefig(f"{params.mnt.analysis_dir}/time_domain_main_voltage.png")

    # Find the last value over the threshold
    last_idx = np.argmax(
        np.abs(time_domain_voltage[:, 1][::-1])
        > max(np.abs(time_domain_voltage[:, 1])) * 0.8
    )
    print(last_idx)
    # Slice and add the time domain voltage
    time_domain_voltage = time_domain_voltage[len(time_domain_voltage) - last_idx :]
    time_domain_voltage[:, 0] -= time_domain_voltage[:, 0][-1]

    # Quick plot of the data
    fig, ax = plt.subplots()
    ax.plot(time_domain_voltage[:, 0], time_domain_voltage[:, 1])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    fig.savefig(f"{params.mnt.analysis_dir}/time_domain_main_voltage_echo.png")

    # Take the fourrier transform of the data
    frequency_domain_voltage, fft_plot = fourier_transform(
        time_domain_voltage[:, 1],
        len(time_domain_voltage[:, 1]),
        int(params.input.sampling_rate),
        plot=True,
    )

    fft_plot.savefig(f"{params.mnt.analysis_dir}/frequency_domain_voltage_main.png")
    np.savetxt(
        f"{params.mnt.analysis_dir}/frequency_domain_voltage_main.csv",
        frequency_domain_voltage,
        delimiter=",",
        encoding="utf-8",
        header="frequencies (Hz), magnitude",
    )

    times = time_domain_voltage[:, 0]

    # Slide a rms window over the data
    params.proc.window_size = 100
    rms_time_domain_voltage = windowed_rms(
        time_domain_voltage[:, 1], params.proc.window_size
    )

    times: np.ndarray = (
        times[int(params.proc.window_size / 2) : int(-params.proc.window_size / 2)]
        + params.proc.window_size / params.input.sampling_rate
    )

    # Quick plot of the rms data
    fig, ax = plt.subplots()
    ax.plot(times, rms_time_domain_voltage)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RMS Voltage (V)")
    fig.savefig(f"{params.mnt.analysis_dir}/time_domain_main_rms_echo.png")

    # Define the gaussian function
    def gaussian(x, a, x0, sigma, b):
        return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2)) + b

    times = times - times[0]

    # Guess the parameters of the gaussian
    a = np.max(rms_time_domain_voltage)
    x0 = times[np.argmax(rms_time_domain_voltage)]
    sigma = (times[-1] - times[0]) / 10  # Approximate width as 1/10th of the range
    b = np.min(rms_time_domain_voltage)

    # Fit the data to a gaussian
    result = curve_fit(
        gaussian, times, rms_time_domain_voltage, p0=[a, x0, sigma, b], maxfev=10000
    )

    a_opt, x0_opt, sigma_opt, b_opt = result[0]

    # Report the results
    logging.info("The fit parameters are:")
    logging.info("a: %s", a_opt)
    logging.info("x0: %s", x0_opt)
    logging.info("sigma: %s", sigma_opt)
    logging.info("b: %s", b_opt)

    # Quick plot of the rms data
    fig, ax = plt.subplots()
    ax.plot(times, rms_time_domain_voltage)
    ax.plot(times, gaussian(times, *result[0]), label="fit")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RMS Voltage (V)")
    fig.savefig(f"{params.mnt.analysis_dir}/time_domain_main_rms_echo_fit.png")

    times = time_domain_voltage[:, 0] - time_domain_voltage[:, 0][0]

    # Using the fit parameters to isolate the echo from the data
    t1_echo = x0_opt - 3 * sigma_opt
    t2_echo = x0_opt + 3 * sigma_opt
    mask = (times > t1_echo) & (times < t2_echo)
    echo_time_domain_voltage = time_domain_voltage[mask]

    # Quick plot of the echo
    fig, ax = plt.subplots()
    ax.plot(echo_time_domain_voltage[:, 0], echo_time_domain_voltage[:, 1])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    fig.savefig(f"{params.mnt.analysis_dir}/time_domain_echo_voltage_after_fit.png")

    # Save the echo
    np.savetxt(
        f"{params.mnt.analysis_dir}/echo_time_domain_voltage.csv",
        echo_time_domain_voltage,
        delimiter=",",
        encoding="utf-8",
        header=f"""mean of abs voltage: {np.mean(np.abs(echo_time_domain_voltage[:, 1]))}\n
        max of voltage: {np.max(echo_time_domain_voltage[:, 1])}\n
        min of voltage: {np.min(echo_time_domain_voltage[:, 1])}\n
        time since start (s), voltage (V)
        """,
    )

    # Save the fit parameters
    np.savetxt(
        f"{params.mnt.analysis_dir}/fit_parameters.csv",
        result[0],
        delimiter=",",
        encoding="utf-8",
        header="a, x0, sigma, b",
    )

    # Take a fourrier transform of the echo
    frequency_domain_voltage, fft_plot = fourier_transform(
        echo_time_domain_voltage[:, 1],
        len(echo_time_domain_voltage[:, 1]),
        int(params.input.sampling_rate),
        plot=True,
    )

    fft_plot.savefig(f"{params.mnt.analysis_dir}/frequency_domain_voltage_echo.png")
    np.savetxt(
        f"{params.mnt.analysis_dir}/frequency_domain_voltage_echo_after_fit.csv",
        frequency_domain_voltage,
        delimiter=",",
        encoding="utf-8",
        header="frequencies (Hz), magnitude",
    )

    # Load the data
    time_domain_voltage = np.loadtxt(
        f"{params.mnt.data_dir}/time_domain_voltage.csv", delimiter=","
    )

    split_time = 0.019
    end_split_time = 0.023

    # Split the data into the main signal before and after the
    # split times and the echo between split times
    main_signal = time_domain_voltage[time_domain_voltage[:, 0] < split_time]
    echo = time_domain_voltage[
        (time_domain_voltage[:, 0] > split_time)
        & (time_domain_voltage[:, 0] < end_split_time)
    ]

    # Plot the data with
    fig, ax = plt.subplots()
    ax.plot(
        main_signal[:, 0] * 1000,
        main_signal[:, 1],
        label="Main Signal",
        color="#8DC353",
    )
    ax.plot(echo[:, 0] * 1000, echo[:, 1], label="Echo", color="#1C458A")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage (V)")
    ax.grid(True)
    ax.set_title("Expected Spin Echo Data")
    fig.savefig(f"{params.mnt.analysis_dir}/expected_time_domain_main_voltage.png")


    # Calculate the decay time of the echo
    decay_time = 2 * sigma_opt
    

    # Calculate the magnitude of the echo
    echo_magnitude = np.mean(np.abs(echo[:, 1]))

    


    # Report the magnitude of the echo
    logging.info("The magnitude of the echo is: %s", echo_magnitude)

    return decay_time, echo_magnitude



if __name__ == "__main__":

    parameters = config.Parameters()
    example_data_path = "data/spin_echo/fake/2128_kHz/time_domain_voltage.csv"  # Add the path to the example data
    with open(example_data_path, "r", encoding="utf-8") as example_data_file:
        example_data = np.loadtxt(example_data_file, delimiter=",", encoding="utf-8")
    decay_time, echo_magnitude = run(parameters, time_domain_voltage=example_data)
    print(f"Decay time of the echo: {decay_time}")
    print(f"Magnitude of the echo: {echo_magnitude}")
