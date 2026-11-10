"""
This script is used to run the spin echo measurement, processing and analysis.
"""

import os
import sys

import numpy as np

# Get the grand grand parent diractory relative to this file
# If the sourc directory is not in the sys.path, add it
source_dir =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if source_dir not in sys.path:
    sys.path.append(source_dir)
    sys.path.append(os.path.join(source_dir, "src"))

# pylint: disable=wrong-import-position
# pylint: disable=import-error
from config.spin_echo import Parameters
from free_spin_decay import measurement
from free_spin_decay import processing
from free_spin_decay import analysis

# Defining parameters
parameters: Parameters = Parameters()

frequencies = np.linspace(
    parameters.pulse.center_freq - parameters.pulse.bandwidth / 2,
    parameters.pulse.center_freq + parameters.pulse.bandwidth / 2,
    num=parameters.run.resolution,
)

for frequency in frequencies:
    for repeat in range(parameters.run.mnt_repeats):
        parameters.mnt.frequency = frequency
        parameters.mnt.repeat = repeat
        parameters.run.label = f"free_spin_decay_{frequency}_{repeat}"
        time_domain_voltage = measurement.run(parameters, frequency, repeat)
        processed_time_domain_voltage = processing.run(
            parameters, time_domain_voltage, frequency, repeat
        )
        analysis.run(parameters, data=processed_time_domain_voltage)
        print(f"Finished {parameters.run.label}")
