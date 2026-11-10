"""Measurement script for paramagnetic magnitude measurement"""
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
from config.paramagnetic import Parameters
from src.free_spin_decay import measurement as fsd_measurement


def run(
    p: Parameters, frequency: Union[float, None] = None, repeat: Union[int, None] = None
) -> np.ndarray:
    """Run the paramagnetic magnitude measurement

    Args:
        p: The parameters of the experiment
        frequency: The frequency of the experiment if None the default frequency is used
        repeat: The repeat number of the experiment if None no repeat is used
    
    Returns:    
        The time domain voltage data
    """
    voltage_data = fsd_measurement.run(p, frequency, repeat)
    return voltage_data


if __name__ == "__main__":
    params = Parameters()
    time_domain_voltage = run(params)
    # Quick plot
    plt.plot(time_domain_voltage)
    plt.show()
