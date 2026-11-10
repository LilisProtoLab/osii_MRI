"""
This script is used to run the spin echo measurement, processing and analysis.
"""

import os
import sys


# If the sourc directory is not in the sys.path, add it
source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if source_dir not in sys.path:
    sys.path.append(source_dir)
    sys.path.append(os.path.join(source_dir, "src"))

# pylint: disable=wrong-import-position
from config.spin_echo import Parameters
from spin_echo import measurement
from spin_echo import processing
from spin_echo import analysis

# Defining parameters
parameters: Parameters = Parameters()

time_domain_voltage = measurement.run(parameters)
processed_time_domain_voltage, frequency_domain_voltage = processing.run(
    parameters, time_domain_voltage
)
analysis.run(parameters, processed_time_domain_voltage)
print(f"Finished {parameters.run.label}")
