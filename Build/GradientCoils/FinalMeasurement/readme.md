# Field Measurement and Validation

## Setup

To validate our coil, we measured the resulting field using the TMAG5273 (see the [HallProbe](../HallProbe/) folder).

## Measurement Results

We connected the coil to a 3A current source and moved the hall probe inside the coil, moving it up and down before taking it outside. A field difference of approximately 6 mT over 10 cm was measured, aligning with our expectation of ~2 mT/m/A. The measurement results are available in [output.csv](output.csv) and [measurement.png](../Images/measurement.png). We measured the magnetic field in the Z-direction by first inserting the hall probe into the coil, then moving it up and down, and finally removing the hall probe. The positions are marked by numbers in [measurement.png](../Images/measurement.png).

**Note:** The axes of the Hall probe outputs do not correspond to the coil's coordinate system. Y of the hall probe aligns with Z of the cylinder, Z with X, and X with Y.
