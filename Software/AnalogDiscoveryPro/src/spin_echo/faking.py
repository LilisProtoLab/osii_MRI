"""
This script is used to generate a fake spin echo signal. It is used to test the
processing of the spin echo signal.
"""

import os
import sys

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
    prepare_all_directories,
    set_frequency_and_label,
)
from config.spin_echo import Parameters
from spin_echo import measurement


# Defining parameters
parameters: Parameters = Parameters()
parameters.run.label = "spin_echo_fake"

# The important times
t1 = parameters.pulse.duration / 2  # End of the pi/2 pulse
t2 = t1 + parameters.pulse.wait_time  # End of the wait time, start of the pi pulse
t3 = t2 + parameters.pulse.duration  # End of the pi pulse
t4 = t3 + parameters.pulse.wait_time  # End of the wait time, start of the echo pulse
t5 = t4 + parameters.pulse.duration / 2  # Center of the echo pulse
t_end = t5 + parameters.pulse.duration / 2 + 0.005 # End of the echo pulse

# Generate the time domain voltage
number_of_points = int(parameters.input.sampling_rate * t_end)
time_domain_voltage = np.zeros((number_of_points, 2))
time_domain_voltage[:, 0] = np.linspace(0, t_end, number_of_points)

# Generate a sin wave at the center frequency
time_domain_voltage[:, 1] = np.sin(
    2 * np.pi * parameters.pulse.center_freq * time_domain_voltage[:, 0]
)



# Create masks for important times
mask1 = (time_domain_voltage[:, 0] > t1) & (time_domain_voltage[:, 0] < t2)
mask2 = time_domain_voltage[:, 0] > t3

# Set the generated sin wave to zero at the important times
time_domain_voltage[mask1, 1] = 0
time_domain_voltage[mask2, 1] = 0


# Add Gaussian noise
time_domain_voltage[:, 1] += np.random.normal(0, 0.005, time_domain_voltage.shape[0])

mask = np.abs(time_domain_voltage[:, 1]) < 0.5
time_domain_voltage = time_domain_voltage[mask]

first_time = t5 - parameters.pulse.duration / 2
last_time = t5 + parameters.pulse.duration / 2

# Add a fake echo as a gaussian envoloped sine wave
A = 0.07
fake_echo = np.zeros_like(time_domain_voltage[:, 1])
fake_echo += A * np.sin(
    2 * np.pi * parameters.pulse.center_freq * (time_domain_voltage[:, 0] - t5)
)
fake_echo *= np.exp(
    -(((time_domain_voltage[:, 0] - t5) / (parameters.pulse.duration)) ** 2)
)
time_domain_voltage[:, 1] += fake_echo

# Save the data
parameters.run.label = "fake"
set_frequency_and_label(parameters)
prepare_all_directories(parameters)


np.savetxt(
    f"{parameters.mnt.data_dir}/time_domain_voltage.csv",
    time_domain_voltage,
    delimiter=",",
    encoding="utf-8",
    header=f"""mean of abs voltage: {np.mean(np.abs(time_domain_voltage[:, 1]))}\n
    max of voltage: {np.max(time_domain_voltage[:, 1])}\n
    min of voltage: {np.min(time_domain_voltage[:, 1])}\n
    time since start (s), voltage (V)
    """,
)

# Quick plot
plt.plot(time_domain_voltage[:, 0], time_domain_voltage[:, 1])
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.title("Spin echo signal")
plt.savefig(f"{parameters.mnt.result_dir}/time_domain_voltage_fig.png")
plt.show()
# fig.savefig(f"results/{parameters.run.label}/FAKE_time_domain_voltage_fig.png")
