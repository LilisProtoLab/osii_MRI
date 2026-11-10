"""Analysis of the paramagnetic data"""

import os
import sys
from typing import Union, Tuple

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
    filter_out_edges_time_domain,
    prepare_all_directories,
)
from config import paramagnetic as config


def run(
    params: config.Parameters,
    data: np.ndarray = None,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> Tuple[float, float]:
    """Runs the analysis of the paramagnetic data"""

    # Set the frequency, if not set use the default frequency
    set_frequency_and_label(params, frequency, repeat)

    print(params.mnt.label)

    # Prepare the directories
    prepare_all_directories(params, frequency, repeat)

    if data is None:
        time_domain_voltage = np.loadtxt(
            f"{params.mnt.data_dir}/filtered_time_domain_voltage.csv",
            delimiter=",",
            encoding="utf-8",
        )
    else:
        time_domain_voltage = data

    filtered_time_domain_voltage = filter_out_edges_time_domain(time_domain_voltage)

    rms_voltage_list = []

    # Calculate the root mean square of a window slide over the time domain voltage
    params.proc.window_size = 10
    for j in range(
        0,
        len(filtered_time_domain_voltage) - params.proc.window_size,
        params.proc.window_size,
    ):
        rms_voltage = np.sqrt(
            np.mean(
                filtered_time_domain_voltage[j : j + params.proc.window_size, 1] ** 2
            )
        )
        # Append the root mean square voltage to the list
        rms_voltage_list.append(rms_voltage)

    # Remove NaN values
    rms_voltage_list = [x for x in rms_voltage_list if str(x) != "nan"]

    # Convert the lists to numpy arrays
    rms_voltage_list = np.array(rms_voltage_list)

    # Slice the times to fit the window size
    windowed_times = (
        filtered_time_domain_voltage[: len(rms_voltage_list), 0]
        - filtered_time_domain_voltage[0, 0]
    )

    # Quick plot
    plt.figure()
    plt.plot(
        windowed_times,
        rms_voltage_list,
        label=f"Null signal: mean = {np.mean(rms_voltage_list):.2e}",
    )
    # Report the mean    plt.xlabel("Time [s]")
    plt.ylabel("RMS voltage [V]")
    plt.title(f"RMS voltage of null and sample signal for {params.mnt.label}")
    plt.legend()
    plt.savefig(f"{params.mnt.analysis_dir}/rms_voltage.png")

    # Report the results
    print(params.mnt.label)
    print(f"Mean magnitude signal: = {np.mean(rms_voltage_list):.2e}")

    return np.mean(rms_voltage_list), np.std(rms_voltage_list)


if __name__ == "__main__":

    # Load the parameters
    p = config.Parameters()

    example_data_path = "data/paramagnetic/file_sample/2128_kHz_1/filtered_time_domain_voltage.csv"

    # Load the data
    with open(
        example_data_path,
        "r",
        encoding="utf-8",
    ) as example_file:
        voltage_data = np.loadtxt(example_file, delimiter=",")

    magnitude, standard_deviation = run(p, data=voltage_data)
    print(f"Mean: {magnitude}")
    print(f"Standard deviation: {standard_deviation}")
