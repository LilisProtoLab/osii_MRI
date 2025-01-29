"""
This script is used to run the spin echo measurement. It is called by the run script.
"""

import os
import sys
import time
from typing import Union

import logging
import numpy as np
import matplotlib.pyplot as plt
from labphew.controller.digilent import waveforms

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
    prepare_all_directories,
    initialize_logger,
    report_max_mean_min,
    plot_time_domain_voltage,
)
from src._dwf.utils import (
    configure_out_channel,
    configure_in_channel,
    get_max_buffer_size,
)
from config.spin_echo import Parameters


def run(
    params: Parameters,
    frequency: Union[float, None] = None,
    repeat: Union[int, None] = None,
) -> tuple[np.ndarray, list[float]]:
    """Runs the spin echo measurement with the given parameters.

    Args:
        params: The parameters of the experiment
        frequency: The frequency of the experiment if None the default frequency is used
        repeat: The repeat number of the experiment if None no repeat is used

    Returns:
        The time domain voltage data and the important times of the experiment
    """
    # Everything logging.infoed to the console is saved in a log file
    set_frequency_and_label(params, frequency, repeat)
    print(params.mnt.label)
    prepare_all_directories(params, frequency, repeat)

    initialize_logger("results", params.run.label)
    params.output.run_time = float(params.mnt.duration)
    # Finding and listing al connected devices
    devs = waveforms.enumerate_devices()
    waveforms.print_device_list(devs)

    # Picking and defining device
    ad_pro = waveforms.DfwController(params.dwf.device, params.dwf.config)

    # params.input.sampling_rate = int(1e6)
    params.input.buffer_size = get_max_buffer_size(
        ad_pro.ai, params.mnt.duration, sampling_rate=params.input.sampling_rate
    )

    # Setting up the device
    configure_out_channel(ad_pro, params.output)
    configure_in_channel(ad_pro, params.input)  # Input channel configuration

    ad_pro.DigitalIO.outputEnableSet(
        params.mnt.bit_mask_output
    )  # Setting up digital IO pins for output, controlling the switches

    # Setting up the digital IO to low prior to the measurement
    ad_pro.DigitalIO.outputSet(params.mnt.bit_mask_s0)

    # Start the measurement
    ad_pro.ai.configure(
        True, 1
    )  # Start the acquisition, by setting the configured AI channel to active
    start_time = time.time()  # Start time of the measurement
    ad_pro.ao.configure(
        0, 1
    )  # Start the output, by setting the configured AO channel to active
    ad_pro.DigitalIO.outputSet(params.mnt.bit_mask_s1)  # Let the signal trhoug the amp

    time.sleep(params.pulse.duration / 2)  # Wait for the duration of the pulse

    t_end_half_pi_pulse = time.time()

    ad_pro.DigitalIO.outputSet(
        params.mnt.bit_mask_s0
    )  # Stop the signal reaching the amp

    time.sleep(params.pulse.wait_time)  # Wait for the duration of the pulse

    t_start_pi_pulse = time.time()

    ad_pro.DigitalIO.outputSet(
        params.mnt.bit_mask_s1
    )  # Let the signal reaching the amp

    time.sleep(params.pulse.duration)  # Wait for the duration of the pulse

    t_end_pi_pulse = time.time()

    ad_pro.DigitalIO.outputSet(params.mnt.bit_mask_s0)  # Set all IO pins to low

    ad_pro.wait_for_ai_acquisition()  # Let the buffer fill

    end_time = time.time()  # End time of the measurement
    ad_pro.ai.configure(False, 0)  # Stop the acquisition
    ad_pro.ao.configure(0, 0)  # Stop the output
    important_times = [
        start_time,
        t_end_half_pi_pulse,
        t_start_pi_pulse,
        t_end_pi_pulse,
        end_time,
    ]
    # %%---------------------------------------------------------------------------
    # The measurement is done, now we can start processing the data

    # Retrieve valid samples
    logging.info("The measurement took %s", end_time - start_time)
    t = np.linspace(0, end_time - start_time, num=params.input.buffer_size)
    if params.input.channel == -1:
        scope1 = ad_pro.ai.statusData(0, params.input.buffer_size)
        scope2 = ad_pro.ai.statusData(1, params.input.buffer_size)
        scope1 = np.array(scope1)
        scope2 = np.array(scope2)
        data_stack = np.column_stack([t, scope1, scope2])
    else:
        scope = ad_pro.ai.statusData(params.input.channel, params.input.buffer_size)
        scope = np.array(scope)
        data_stack = np.column_stack([t, scope])

    return data_stack, important_times


# only run the code if it is the main file
if __name__ == "__main__":
    parameters: Parameters = Parameters()
    time_domain_voltage, _ = run(parameters)
    print("Data acquisition done")
    report_max_mean_min(time_domain_voltage[:, 1])

    # Quick plot of the data
    fig, axs = plot_time_domain_voltage(
        time_domain_voltage[:, 1],
        time_domain_voltage[:, 0],
        input_config=parameters.input,
        label=parameters.run.label,
    )
    plt.show()
    print("Plotting done")
