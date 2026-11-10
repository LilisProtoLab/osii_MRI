"""
This script is used to run the spin echo measurement, processing and analysis.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Get the grand grand parent diractory relative to this file
# If the sourc directory is not in the sys.path, add it
source_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if source_dir not in sys.path:
    sys.path.append(source_dir)
    sys.path.append(os.path.join(source_dir, "src"))

# pylint: disable=wrong-import-position
# pylint: disable=import-error
from config.spin_echo import Parameters
from paramagnetic import measurement
from paramagnetic import processing
from paramagnetic import analysis

# Defining parameters
parameters: Parameters = Parameters()

frequencies = np.linspace(
    parameters.pulse.center_freq - parameters.pulse.bandwidth / 2,
    parameters.pulse.center_freq + parameters.pulse.bandwidth / 2,
    num=parameters.run.resolution,
)

freq_mean_list = []
freq_std_list = []

for frequency in frequencies:
    mean_repeat_list = []
    std_repeat_list = []

    for repeat in range(parameters.run.mnt_repeats):
        parameters.mnt.frequency = frequency
        parameters.mnt.repeat = repeat
        parameters.run.label = f"free_spin_decay_{frequency}_{repeat}"
        time_domain_voltage = measurement.run(parameters, frequency, repeat)
        processed_time_domain_voltage = processing.run(
            parameters, time_domain_voltage, frequency, repeat
        )
        mean_, std_ = analysis.run(parameters, processed_time_domain_voltage)
        mean_repeat_list.append(mean_)
        std_repeat_list.append(std_)
        print(f"Finished {parameters.run.label}")

    freq_mean_list.append(np.mean(mean_repeat_list))
    freq_std_list.append(np.mean(std_repeat_list))

# Plot the rms data points
plt.figure()
plt.errorbar(
    range(1, len(freq_mean_list) + 1),
    freq_mean_list,
    yerr=freq_std_list,
    fmt="o",
    label="Signal",
)
plt.xlabel("Measurement number")
plt.ylabel("RMS voltage [V]")
plt.legend()
plt.savefig(f"{parameters.run.analysis_dir}/mean_voltage.png")

# Report the results
mean_rms_voltage = np.mean(freq_mean_list)
std_rms_voltage = np.mean(freq_std_list)
print(
    f"The mean rms voltage of the null signal is {mean_rms_voltage} with a standard deviation of {std_rms_voltage}"
)

# Save the results
with open(f"{parameters.run.analysis_dir}/rms_voltage.txt", "w", encoding="utf-8") as f:
    f.write(
        f"The mean rms voltage of the null signal is {mean_rms_voltage}\
            with a standard deviation of {std_rms_voltage}\n"
    )
