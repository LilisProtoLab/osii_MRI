"""Processes the time domain voltage data and saves the results."""

import os
import sys
import logging
from typing import Union

import numpy as np
import matplotlib.pyplot as plt

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
    report_max_mean_min,
    fourier_transform,
    prepare_all_directories,
    initialize_logger
)
from config.spin_echo import Parameters


def run(
    params: Parameters,
    voltage_data: np.ndarray[np.float64, np.float64],
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Processes the time domain voltage data and saves the results.

    Args:
        params: The parameters of the experiment
        voltage_data: The time domain voltage data
        frequency: The frequency of the experiment if None the default frequency is used
        repeat: The repeat number of the experiment if None no repeat is used

    Returns:
        The time domain voltage data and the frequency domain voltage data
    """
    # Set the frequency, if not set use the default frequency
    set_frequency_and_label(params, frequency, repeat)
    prepare_all_directories(params, frequency, repeat)
    initialize_logger("results", params.run.label)
    # Removing padded zeros from data
    voltage_data = voltage_data[np.abs(voltage_data[:, 1]) > params.proc.epsilon]
    # Defining directories
    mean_, max_, min_ = report_max_mean_min(voltage_data[:, 1])

    np.savetxt(
        f"{params.mnt.data_dir}/time_domain_voltage.csv",
        voltage_data,
        delimiter=",",
        encoding="utf-8",
        header=f"""mean of abs voltage: {mean_}\n
    max of voltage: {max_}\n
    min of voltage: {min_}\n
    time since start (s), voltage (V)
    """,
    )

    # Plotting the time domain voltage
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(
        voltage_data[:, 0] / 1000,
        voltage_data[:, 1],
        color="#8DC353",
        label="Voltage",
    )
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage (V)")
    ax.grid(True)
    ax.set_title("Generated Spin Echo Data")
    ax.legend()
    fig.savefig(f"{params.mnt.result_dir}/time_domain_voltage_fig.png")
    logging.info(
        "Saved time_domain_voltage figure at %s/time_domain_voltage_fig.png",
        params.mnt.result_dir,
    )

    ax.set_xlim(params.proc.time_domain_zoom)
    fig.savefig(f"{params.mnt.result_dir}/time_domain_voltage_zoomed_fig.png")
    logging.info(
        "Saved time_domain_voltage zoomed figure at %s/time_domain_voltage_zoomed_fig.png",
        params.mnt.result_dir,
    )

    # Taking the fourrier transform
    freq_domain_voltage, fft_plot = fourier_transform(
        voltage_data[:, 1],
        len(voltage_data[:, 1]),
        int(params.input.sampling_rate),
        plot=True,
    )
    if fft_plot is not None:
        fft_plot.savefig(f"{params.mnt.result_dir}/frequency_domain_voltage_figure.png")

    logging.info(
        "Saved frequency_domain_voltage figure at %s/frequency_domain_voltage_figure.png",
        params.mnt.result_dir,
    )

    np.savetxt(
        f"{params.mnt.data_dir}/frequency_domain_voltage.csv",
        freq_domain_voltage,
        delimiter=",",
        encoding="utf-8",
        header="frequencies (Hz), magnitude",
    )
    logging.info(
        "Saved frequency_domain_voltage_figure at %s/time_domain_voltage.csv",
        params.mnt.data_dir,
    )

    return voltage_data, freq_domain_voltage


if __name__ == "__main__":
    print("Running spin echo processing")
    parameters: Parameters = Parameters()

    example_data_path = "data/spin_echo/fake/2128_kHz/time_domain_voltage.csv"
    with open(example_data_path, "r", encoding="utf-8") as example_file:
        time_domain_voltage = np.loadtxt(example_file, delimiter=",", encoding="utf-8")

    time_domain_voltage, frequency_domain_voltage = run(parameters, time_domain_voltage)
