# CoilDesign Source Code

This folder contains the source code for generating gradient coil designs.
gradient coil design
## Files

- `generate_gradients.m`: MATLAB script for designing z-gradient coil.
- `generate_gradients.py`: Python script for designing x and y gradient coils.

## General remarks
Both files have the same functionality. For the given project the z- gradient coil was designed with the MATLAB version, x and y gradient coils with the Python version. We started with the MATLAB version, however the Python version seemed to be less memory intensive especially when setting a high smooth factor, which was a reason for us to switch to python. 

## Known Issues
We encountered problems when using "FastHenry" for inductance calculations. One solution was by running the code without installing FastHenry (which is part of FastFieldSolvers). Another solution is to increase the waiting time in the `calculate_inductance_by_coil_layout`   function (increase the number in `Wscript.Sleep 500` (holds for CoilGen and PyCoilGen)). This was discussed in an [Issue](https://github.com/kev-m/pyCoilGen/issues/76) with the developer of PyCoilGen:

Another problem occured in PyCoilGen when the meshes were improted into Fusion. An error stated that the meshes have a non positive volume. This can be fixed by reversing the point order in crossectional points. (Also this was also discussed in an [Issue](https://github.com/kev-m/pyCoilGen/issues/75) with the developer of PyCoilGen)



