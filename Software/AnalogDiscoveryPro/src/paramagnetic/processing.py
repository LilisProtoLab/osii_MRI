"""Contains the processing script for the paramagnetic data."""

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
from src.utils import prepare_all_directories, set_frequency_and_label
from config import paramagnetic as config


def run(
    params: config.Parameters,
    data: Union[np.ndarray, None] = None,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> np.ndarray:
    """Runs the analysis of the paramagnetic data

    Args:
        params: The parameters of the experiment
        data: The time domain voltage data of the signal. If None the data is loaded from file
        frequency: The frequency of the experiment
        repeat: The repeat number of the experiment

    Returns:
        The processed time domain voltage data of the signal
    """

    # Set the frequency, if not set use the default frequency
    set_frequency_and_label(params, frequency, repeat)

    print(params.mnt.label)

    # Prepare the directories
    prepare_all_directories(params, frequency, repeat)

    if data is None:
        if not os.path.isfile(
            f"{params.mnt.data_dir}/{params.mnt.label}/time_domain_voltage.csv"
        ):
            print(
                f"{params.mnt.data_dir}/{params.mnt.label}/time_domain_voltage.csv not found"
            )
            return None
        time_domain_voltage = np.loadtxt(
            f"{params.mnt.data_dir}/{params.mnt.label}/time_domain_voltage.csv",
            delimiter=",",
        )
    else:
        time_domain_voltage = data

    mask1 = (
        time_domain_voltage[:, 0] > 0.1
    )  # Filters out the first 0.1 seconds wherin the signal is not stable
    mask2 = (
        time_domain_voltage[:, 1] > 2e-2
    )  # Filter out the part of the signal where the signal is too small
    mask = mask1 & mask2

    filtered_time_domain_voltage = time_domain_voltage[mask]

    first_time_point, last_time_point = (
        filtered_time_domain_voltage[0, 0],
        filtered_time_domain_voltage[-1, 0],
    )
    time_mask = (time_domain_voltage[:, 0] > first_time_point - 0.05) & (
        time_domain_voltage[:, 0] < last_time_point + 0.05
    )
    filtered_time_domain_voltage = time_domain_voltage[time_mask]


    with open( # Save the filtered time domain voltage
        f"{params.mnt.data_dir}/filtered_time_domain_voltage.csv",
        "w",
        encoding="utf-8",
    ) as file:
        np.savetxt(
            file,
            filtered_time_domain_voltage,
            delimiter=",",
        )

    # Quick plot
    plt.figure()
    plt.plot(filtered_time_domain_voltage[:, 0], filtered_time_domain_voltage[:, 1])
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Voltage vs time")
    plt.savefig(f"{params.mnt.analysis_dir}/filtered_time_domain_voltage.png")
    # Drop file from memory
    return filtered_time_domain_voltage


if __name__ == "__main__":

    # Load the parameters
    p = config.Parameters()

    example_data_path = "data/paramagnetic/file_sample/2128_kHz/time_domain_voltage.csv"

    # Load the data
    with open(
        example_data_path,
        "r",
        encoding="utf-8",
    ) as example_file:
        voltage_data = np.loadtxt(example_file, delimiter=",")

    # Run the processing
    filtered_voltage_data = run(p, voltage_data)

    # Quick plot
    plt.figure()
    plt.plot(filtered_voltage_data[:, 0], filtered_voltage_data[:, 1])
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage [V]")
    plt.title("Voltage vs time")
    plt.show()
    plt.close()
