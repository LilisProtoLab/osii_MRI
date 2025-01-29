"""Initializes the dwf module by loading the dwfconstants module dynamically."""
import sys
import os
import ctypes

def load_dwfconstants():
    """Loads the dwfconstants module dynamically."""
    platform = sys.platform
    sep = os.sep

    if platform.startswith("win"):
        # Windows
        _ = ctypes.cdll.dwf
        constants_path = \
        f"C:{sep}Program Files (x86){sep}Digilent{sep}WaveFormsSDK{sep}samples{sep}py"
    elif platform.startswith("darwin"):
        # macOS
        lib_path = f"{sep}Library{sep}Frameworks{sep}dwf.framework{sep}dwf"
        _ = ctypes.cdll.LoadLibrary(lib_path)
        constants_path = \
        f"{sep}Applications{sep}WaveForms.app{sep}Contents{sep}Resources{sep}SDK{sep}samples{sep}py"
    else:
        # Linux
        _ = ctypes.cdll.LoadLibrary("libdwf.so")
        constants_path = f"{sep}usr{sep}share{sep}digilent{sep}waveforms{sep}samples{sep}py"

    # Append the constants path to the system path
    sys.path.append(constants_path)

    # Import the dwfconstants dynamically
    # pylint: disable=import-outside-toplevel
    # pylint: disable=import-error
    import dwfconstants as constants
    return constants
