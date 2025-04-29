# Shim Optimization

Note: All positions are relative to the isocenter of the permanent magnet assembly (the center of the imaging volume), which is typically the geometric center of the magnet assembly. Shim magnet positions correspond to the location of the geometric center of the shim magnet.

## Algorithms

### `NIST_shim.py` 

A _very slow_ genetic algorithm. Not recommended at this time.

### `NIST_fast_shim.py`

A  _much faster_ magnet-wise optimization algorithm, and is the presently recommended solution. It has the following options:

`cost_fn` - Either `ptp` to minimize peak-to-peak variation in B0, or `std` to minimize the standard deviation

`generate_shim` - `True` runs the shim generation algorithm. `False` attempts to load an existing shim for analysis from `shim_out_fname`

`B0_nom` - nominal field strength of magnet (in T)

`n_passes` - passes through magnet optimization. 3 seems to work well

`n_angles` - possible angles for shim magnet. 4 seems to work reasonably well, although it may be worth trying more

Magnet properties: the magnetization of the magnet needs to be specified in A/m. The N56 magnets NIST is using have a magnetization of 1185704 A/m.

## Inputs

### Magnet Positions - `mag_pos_fname`

CSV with positions of potential magnets positions in the following format:

| X   | Y   | Z   |
|-----|-----|-----|
| x_0 | y_0 | z_0 |
| x_1 | y_1 | z_1 |

Two magnet position files are included for use with the OSII Mini:
 - OSII_MINI - all slots in the shim trays are included with 18 positions per cartridge (2410 possible positions)
 - OSII_MINI_reduced - every other shim tray slot is included, with 10 positions per cartridge (680 possible positions)

### B0 Map - `b0_map_fname`

CSV with B0 field map in the following format:

| X   | Y   | Z   | B_0  |
|-----|-----|-----|------|
| x_0 | y_0 | z_0 | B0_0 |
| x_1 | y_1 | z_1 | B0_1 |

B0 is in T

The shim design will be optimized by the same point that are included in the B0 map, so it is advisable to limit the B0 map to the outer shell in order to speed up the computation. The script in `b0_map_shell.py` can be used to reduce a full map to only the outer shell.

## Outputs

### Optimal Shim - `shim_out.csv`

CSV specifying whether a magnet should be placed at each position, and if so, at what angle.

| X   | Y   | Z   | Place   | Angle   |
|-----|-----|-----|---------|---------|
| x_0 | y_0 | z_0 | place_0 | angle_0 |
| x_1 | y_1 | z_1 | place_1 | angle_1 |

Place is True or False

### Optimization result - `optimization_results.pickle`

**Only for Genetic Algorithm**

Pickle file with all optimization results. For more detail on what this includes, please consult the [pymoo documentation](https://pymoo.org/interface/result.html?highlight=results).