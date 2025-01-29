"""This module contains the functions to perform a Free Spin Decay (FSD) measurement"""

import os
import sys
import time
from typing import Union

import logging
import numpy as np
from matplotlib import rcParams
import matplotlib.pyplot as plt

from labphew.controller.digilent import waveforms

# If the sourc directory is not in the sys.path, add it
source_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
if source_dir not in sys.path:
    sys.path.append(source_dir)

# pylint: disable=wrong-import-position
from src.utils import (
    initialize_logger,
    prepare_all_directories,
    set_frequency_and_label,
)
from src._dwf.utils import (
    configure_out_channel,
    configure_in_channel,
    get_max_buffer_size,
)
from config import free_spin_decay as config

# Increase the chunk size for the plot to avoid memory errors
rcParams["agg.path.chunksize"] = 10000


def run(
    params: config.Parameters,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> np.ndarray:
    """Run the Free Spin Decay measurement

    Args:
        params: The parameters of the experiment
        frequency: The frequency of the experiment if None the default frequency is used
        repeat: The repeat number of the experiment if None no repeat is used
        The time domain voltage data

    """

    # Everything logging.infoed to the console is saved in a log file
    initialize_logger("results", params.run.label)

    # Log the description of the experiment
    logging.info(params.run.desription)

    # Initialize the device
    params.dwf.device = waveforms.DfwController(params.dwf.device, params.dwf.config)
    device: waveforms.DfwController = params.dwf.device

    # Set the frequency, if not set use the default frequency
    set_frequency_and_label(params, frequency, repeat)

    print(params.mnt.label)

    # Prepare the directories
    prepare_all_directories(params, frequency, repeat)

    # Set the maximum buffer size depending on the duration of the measurement
    params.input.buffer_size = get_max_buffer_size(
        device, params.mnt.duration, sampling_rate=params.input.sampling_rate
    )

    # Configure the input and output channels
    configure_out_channel(device, params.output)
    configure_in_channel(device, params.input)

    # Configure the IO outputs and set them to low
    device.DigitalIO.outputEnableSet(params.mnt.bit_mask_output)
    device.DigitalIO.outputSet(params.mnt.bit_mask_s0)

    # Start data acquisition
    start_time = time.time()
    device.ai.configure(True, 1)

    # Wait for the signal to stabilize
    time.sleep(params.mnt.t_pre_signal)

    # Start the signal to the pre amp
    device.DigitalIO.outputSet(params.mnt.bit_mask_s1)

    # Start the output channel
    device.ao.configure(0, 1)

    # Wait for the signal to stabilize - Tom look at this
    time.sleep(5)
    device.wait_for_ai_acquisition()  # Wait for the buffer to fill up

    # Stop data acquisition
    end_time = time.time()
    device.ai.configure(False, 0)  # Stop the input channel
    device.DigitalIO.outputSet(
        params.mnt.bit_mask_s0
    )  # Blockin the signal to the pre amp

    # Log the duration of the measurement
    logging.info("The measurement took %s", end_time - start_time)

    # Interpolate the times to match the buffer size
    t = np.linspace(0, end_time - start_time, num=params.input.buffer_size)

    # Get the data from the scope
    if params.input.channel == -1:  # Get both channels
        scope1 = device.ai.statusData(0, params.input.buffer_size)
        scope2 = device.ai.statusData(1, params.input.buffer_size)
        scope1 = np.array(scope1)
        scope2 = np.array(scope2)
        data_stack = np.column_stack([t, scope1, scope2])
    else:  # Get only one channel
        scope = device.ai.statusData(params.input.channel, params.input.buffer_size)
        scope = np.array(scope)
        data_stack = np.column_stack([t, scope])

    return data_stack


if __name__ == "__main__":
    parameters = config.Parameters()
    parameters.experiment = "test"
    time_domain_voltage = run(parameters)
    # Quick plot
    plt.plot(time_domain_voltage)
    plt.show()
