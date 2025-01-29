"""
The file contains a collection of often used utility functions related to the Digilent Waveforms SDK
"""

import os
import sys
import logging
from typing import Union
import ctypes

from labphew.controller.digilent import waveforms

# If the sourc directory is not in the sys.path, add it
source_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
if source_dir not in sys.path:
    sys.path.append(source_dir)
    sys.path.append(os.path.join(source_dir, "src"))

# pylint: disable=wrong-import-position
import src._dwf.dwfconstants as constants
from config import copy_me as config


def configure_node(
    device: waveforms.DfwController,
    node_config: Union[
        config.Carrier, config.AmplitudeModulation, config.FrequencyModulation, None
    ] = None,
    channel_config: Union[config.OutputChannel, None] = None,
) -> None:
    """Configures the node with the given configuration

    Args:
        device: The device to configure
        node_config: The configuration of the node
        channel_config: The configuration of the channel

    Returns:
        None"""
    if node_config.enable:
        device.ao.nodeEnableSet(
            node_config.channel, node_config.node, node_config.enable
        )
        if node_config.function == constants.funcCustom and channel_config is not None:
            data_length = len(channel_config.data)
            buffer = (ctypes.c_double * data_length)()
            for index, _ in enumerate(buffer):
                buffer[index] = ctypes.c_double(channel_config.data[index])
            device.ao.nodeDataSet(node_config.channel, node_config.node, buffer)
        device.ao.nodeFrequencySet(
            node_config.channel, node_config.node, node_config.frequency
        )
        device.ao.nodePhaseSet(node_config.channel, node_config.node, node_config.phase)
        device.ao.nodeAmplitudeSet(
            node_config.channel, node_config.node, node_config.amplitude
        )
        device.ao.nodeOffsetSet(
            node_config.channel, node_config.node, node_config.offset
        )
        logging.info(
            """--------------------------------------------------------------
    %s configured with the following parameters:
    enable: %s
    function: %s
    channel out: %s
    frequency: %s
    amplitude: %s
    offset: %s
--------------------------------------------------------------""",
            node_config.__class__.__name__,
            node_config.enable,
            node_config.function,
            node_config.channel,
            node_config.frequency,
            node_config.amplitude,
            node_config.offset,
        )
    else:
        logging.info("%s was not enabled", node_config.__class__.__name__)


def configure_in_channel(
    device: waveforms.DfwController,
    input_config: config.InputChannel,
) -> None:
    """Configures the input channel with the given configuration

    Args:
        device: The device to configure
        input_config: The configuration of the input channel

    Returns:
        None"""
    device.ai.frequencySet(input_config.sampling_rate)
    device.ai.channelRangeSet(input_config.channel, input_config.volts_range)
    device.ai.bufferSizeSet(input_config.buffer_size)
    logging.info(
        """--------------------------------------------------------------
Input channel configured with following parameters:
Channel in: %s
Sampling rate: %s
Buffer size: %s
Range of values: %s
---------------------------------------------------------------""",
        input_config.channel,
        input_config.sampling_rate,
        input_config.buffer_size,
        input_config.volts_range,
    )


def start_in_out_channels(
    device: waveforms.DfwController, **output_config: config.InputChannel
) -> None:
    """Starts the output and input channels with the given configuration
    
    Args:
        device: The device to configure
        output_config: The configuration of the output channels
    
    Returns:
        None"""
    logging.info("\nStarting output and starting acquisition")
    for _, config_values in output_config.items():
        # Configure each channel with the provided channel_out
        device.ao.configure(config_values.channel, 1)
    device.ai.configure(True, -1)
    logging.info("Started acquisition of signal")


def get_max_sampling_freq(
    device: waveforms.DfwController,
    duration: float,
    minimal_sampling_rate: float = 5e5,
    buffer_size: Union[int, None] = None,
) -> float:
    """Calculates the maximum sampling frequency and checks edge cases
    
    Args:
        device: The device to configure
        duration: The duration of the measurement
        minimal_sampling_rate: The minimal sampling rate
        buffer_size: The size of the buffer
        
    Returns:
        The maximum sampling frequency"""
    if buffer_size is None:
        buffer_size = device.ai.bufferSizeInfo()[1]
    print(buffer_size)
    max_sampling_rate = device.ai.frequencyInfo()[1]
    print(max_sampling_rate)
    proposed_sampling_rate = buffer_size / duration
    print(proposed_sampling_rate)
    if proposed_sampling_rate < minimal_sampling_rate:
        logging.info(
            "The proposed sampling rate of %s is to low increase buffer size or decrease duration",
            proposed_sampling_rate,
        )
    proposed_sampling_rate = max(proposed_sampling_rate, minimal_sampling_rate)
    if proposed_sampling_rate > max_sampling_rate:
        logging.info(
            "The proposed sampling rate of %s is to high", proposed_sampling_rate
        )
    proposed_sampling_rate = min(proposed_sampling_rate, max_sampling_rate)
    logging.info(
        "The sampling rate has been set to %s, decrease buffer size or increase duration",
        proposed_sampling_rate,
    )
    return proposed_sampling_rate


def get_max_buffer_size(device: waveforms.DfwController, duration: float, sampling_rate: float = 5e5) -> int:
    """Calculates the maximum buffer size for the given duration and sampling rate
    
    Args:
        device: The device to configure
        duration: The duration of the measurement
        sampling_rate: The sampling rate
        
    Returns:
        The maximum buffer size"""
    min_buffer, max_buffer = device.ai.bufferSizeInfo()
    proposed_buffer = duration * sampling_rate
    proposed_buffer = max(min_buffer, proposed_buffer)
    proposed_buffer = min(max_buffer, proposed_buffer)
    logging.info("Set buffer size to %s", proposed_buffer)
    return int(proposed_buffer)


def configure_out_channel(
    device: waveforms.DfwController, channel_config: config.OutputChannel
) -> None:
    """Configures the output channel and its nodes
    
    Args:
        device: The device to configure
        channel_config: The configuration of the output channel
    
    Returns:
        None"""
    # enable channel
    channel = ctypes.c_int(channel_config.channel - 1)

    device.ao.repeatSet(channel, channel_config.repeat)
    device.ao.runSet(channel, channel_config.run_time)
    device.ao.waitSet(channel, channel_config.wait_time)

    # Configure the nodes
    configure_node(device, channel_config.carrier, channel_config)
    configure_node(device, channel_config.fm, channel_config)
    configure_node(device, channel_config.am, channel_config)
