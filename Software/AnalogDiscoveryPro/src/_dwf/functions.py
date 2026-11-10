"""Python file containing class defining custom function names 
of the DWF Waveform Generator funtions"""

from src._dwf import dwfconstants as constants


class Function:
    """Class defining custom function names of the DWF Waveform Generator funtions"""

    custom = constants.funcCustom
    sine = constants.funcSine
    square = constants.funcSquare
    triangle = constants.funcTriangle
    noise = constants.funcNoise
    dc = constants.funcDC
    pulse = constants.funcPulse
    trapezium = constants.funcTrapezium
    sine_power = constants.funcSinePower
    ramp_up = constants.funcRampUp
    ramp_down = constants.funcRampDown
