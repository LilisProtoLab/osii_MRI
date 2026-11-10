"""This file contains the functions to process the free spin decay signal"""

import os
import sys
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
    isolate_peak,
    filter_peak,
    find_trailing_edge,
    prepare_all_directories,
)
from config import free_spin_decay as config


def run(
    params: config.Parameters,
    time_domain_voltage: Union[np.ndarray, None],
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> np.ndarray:
    """
    Run the processing of the free spin decay experiment
    Args:
        params: The parameters of the experiment
        time_domain_voltage: The time domain voltage data
        frequency: The frequency of the experiment
        repeat: The repeat number of the experiment
    Returns:
        The processed time domain voltage
    """

    # Set the frequency, if not set use the default frequency
    set_frequency_and_label(params, frequency, repeat)

    print(params.mnt.label)

    # Prepare the directories
    prepare_all_directories(params, frequency, repeat)
    # Load the data
    if time_domain_voltage is None:
        if not os.path.isfile(
            f"{params.mnt.data_dir}/{params.mnt.label}/time_domain_voltage.csv"
        ):
            print(
                f"{params.mnt.data_dir}/{params.mnt.label}/time_domain_voltage.csv not found")
            return None
        time_domain_voltage = np.loadtxt(
            f"{params.mnt.data_dir}/{params.mnt.label}/time_domain_voltage.csv", delimiter=","
        )

    # Isolate the peak
    t_start_peak, t_end_peak = isolate_peak(time_domain_voltage)
    print(f"Peak: {t_start_peak} - {t_end_peak}")

    # Save the peak time domain voltage
    peak_time_domain_voltage = filter_peak(
        time_domain_voltage, t_start_peak, t_end_peak
    )
    print(f"Peak length: {peak_time_domain_voltage.shape}")
    with open(
        f"{params.mnt.data_dir}/peak_time_domain_voltage.csv",
        "w",
        encoding="utf-8",
    ) as f:
        np.savetxt(f, peak_time_domain_voltage, delimiter=",")

    # Delete the time domain voltage from memory
    del peak_time_domain_voltage

    # Find the trailing edge
    filtered_time_domain_voltage = find_trailing_edge(time_domain_voltage, t_end_peak)
    print(f"Filtered length: {filtered_time_domain_voltage.shape}")
    with open(
        f"{params.mnt.data_dir}/decay_time_domain_voltage.csv",
        "w",
        encoding="utf-8",
    ) as f:
        np.savetxt(f, filtered_time_domain_voltage, delimiter=",")

    # Delete the peak time domain voltage from memory
    del time_domain_voltage

    # Quick plot
    plt.figure()
    plt.plot(filtered_time_domain_voltage[:, 0], filtered_time_domain_voltage[:, 1])
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.savefig(f"{params.mnt.analysis_dir}/decay_time_domain_voltage.png")
    plt.close()

    # Save the decay time domain voltage
    with open(
        f"{params.mnt.data_dir}/decay_time_domain_voltage.csv",
        "w",
        encoding="utf-8",
    ) as file:
        np.savetxt(file, filtered_time_domain_voltage, delimiter=",")

    return filtered_time_domain_voltage


if __name__ == "__main__":

    parameters = config.Parameters()
    example_data_path = "data/free_spin_decay/null/2128_kHz/time_domain_voltage.csv"  # Add the path to the example data
    with open(example_data_path, "r", encoding="utf-8") as example_data_file:
        example_data = np.loadtxt(example_data_file, delimiter=",", encoding="utf-8")
    processed_example_data = run(parameters, time_domain_voltage=example_data)

    # Quick plot
    plt.plot(processed_example_data[:, 0], processed_example_data[:, 1])
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.show()
