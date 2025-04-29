"""Code to compute permanent magnet shim for a permanent low-field MRI magnet.
This file implements a magnet-wise optimization that runs much more quickly
than the genetic algorithm in NIST_shim.py

Stephen Ogier - October 2024

At present, this code only uses the Z-component of the shim output
    It could be expanded to work with 3-axis b0 map data.
"""

import numpy as np
import pandas as pd
import magpylib as magpy
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import csv

import logging

import time

# Specify files with input data
mag_pos_fname = 'example_data/OSII_MINI_reduced.csv'
b0_map_fname = 'example_data/shell_background_removed_2024_05_07_b0_sphere_100mm_5mm_increment.csv'
shim_out_fname = 'NYU_Shim_reduced_ptp.csv'

# If True, generate shim. If false, attempt to load existing shim from shim_out_fname
generate_shim = True

# Choose cost function
# ptp - minimize max(B0)-min(B0)
# std - minimize std(B0)
cost_fn = 'ptp'

if cost_fn == 'std':
    metric = np.std
elif cost_fn == 'ptp':
    metric = np.ptp
        
# Configuration Options
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

B0_nom = .04567 # T

# Define magnet properties
# Shim magnet magnetization in A/m
magnetization = 1185704 # N56 magnet average
s = 0.003 # side length
cube_dims = (s,s,s)
cube_mag = (0,0,magnetization) # Magnetized in Z direction
logging.info(f'Magnets are cubes with side length {s*1e3} mm')
logging.info(f'Magnets have magnetization {cube_mag} A/m')

# Define optimization options
n_passes = 3 # Number of passes through magnet optimization

n_angles = 4 # Number of possible magnet orientations
angles = list(np.linspace(0,2*np.pi,n_angles,endpoint=False))

# Begin execution
start_time = time.time()

def magnet_pos_angle_import(magnet_pos_fname):
    """Import CSV file of magnet positions.
    CSV has following format:
    X   Y   Z   Angle
    x0  y0  z0  a0
    x1  y1  z1  a1
    ...

    where (x,y,z) is relative to isocenter of magnet
    and Angle is rotation about X axis
    Magnetization is assumed to be along Z
    """
    magnet_pos_angle_df = pd.read_csv(magnet_pos_fname, header=0, names=['X','Y','Z','Angle'])
    logging.info(f'Successful import of magnet position+angle specification: {magnet_pos_fname}')
    return magnet_pos_angle_df

def magnet_pos_import(magnet_pos_fname):
    """Import CSV file of magnet positions.
    CSV has following format:
    X   Y   Z
    x0  y0  z0
    x1  y1  z1
    ...

    where (x,y,z) is relative to isocenter of magnet
    Magnetization is assumed to be along Z
    """
    magnet_pos_df = pd.read_csv(magnet_pos_fname, header=0, names=['X','Y','Z'])
    logging.info(f'Successful import of magnet position+angle specification: {magnet_pos_fname}')
    return magnet_pos_df

def b0_map_import(b0_map_fname, l_unit = 'mm', B_unit = 'T'):
    """Import B0 map CSV file.
    CSV has the following format:
    X   Y   Z   B0
    x0  y0  z0  B0_0
    x1  y1  z1  B0_1
    ...

    All columns after B0 are ignored.
    """
    b0_map_df = pd.read_csv(b0_map_fname, header=0, usecols=[0,1,2,3], names=['X','Y','Z','B0'])
    logging.info(f'Successful import of B0 map: {b0_map_fname}')
    if l_unit == 'mm':
        b0_map_df['X'] = b0_map_df['X'].values*1e-3
        b0_map_df['Y'] = b0_map_df['Y'].values*1e-3
        b0_map_df['Z'] = b0_map_df['Z'].values*1e-3
    
    if B_unit == 'G':
        b0_map_df['B0'] = b0_map_df['B0']/1e4

    return b0_map_df

def generate_magnets(mag_pos_angle):
    """Generate collection of magnets from array of positions
    mag_pos_angle is a Nx4 array with the following format
        x0  y0  z0  angle0
        x1  y1  z1  angle1
    """
    mag_pos = mag_pos_angle[:,:3]
    angles = mag_pos_angle[:,3]
    mag_rot = R.from_euler('x', angles)

    n_magnets = mag_pos.shape[0]

    magnets = magpy.Collection(style_label='magnets')

    for i in range(n_magnets):
        cube = magpy.magnet.Cuboid(position=mag_pos[i,:], orientation=mag_rot[i], dimension=cube_dims, magnetization=cube_mag)
        magnets.add(cube)
    
    return magnets

def generate_grid_YZ(side, npoints):
    """Generate a grid in the YZ plane (at X=0) for plotting fields

    side is length of side of grid in m
    npoints is number of points in grid along Y and Z
    """
    axis = np.linspace(-side/2, side/2, npoints)
    grid = np.array([[(0,y,z) for y in axis] for z in axis])
    return grid

def compute_fields(mag_pos_angle, sensors):
    """Compute fields of magnets specified in sensor array
    mag_pos_angle is a Nx4 array with the following format
        x0  y0  z0  angle0
        x1  y1  z1  angle1
        ...
    sensor_pos is a Nx3 array with the following format
        x0  y0  z0
        x1  y1  z1
        ...
    """
    # Generate magnet position and rotation
    magnets = generate_magnets(mag_pos_angle)
    
    B = magnets.getB(sensors)
    return B

def compute_cost(mag_pos_angle, sensors: magpy.Sensor, b0_map_vals, cost_fn = 'std'):
    """Compute cost function for optimization

    Cost function is presently std dev of sum of shim B field and the b0 map in ppm
    """

    if len(mag_pos_angle) == 0:
        cost = metric(b0_map_vals)
    else:
        B_shim = compute_fields(mag_pos_angle, sensors)
        B_combined = B_shim[:,2]+b0_map_vals # Add Z-component of shim fields to mapped magnet
        cost = metric(B_combined,0)

    cost = cost/B0_nom*1e6
    
    # print(f'Cost: {cost:.0f} ppm')
    return cost

def gen_sensors(b0_map_df):
    """Generate sensors based on positions of B0 map
    """
    sensor_pos = b0_map_df.to_numpy()[:,:3]
    n_sensors = sensor_pos.shape[0]
    
    sensors = magpy.Collection(style_label='sensors')
    for i in range(n_sensors):
        sensor = magpy.Sensor(sensor_pos[i,:])
        sensors.add(sensor)
    
    return sensors

magnet_pos_df = magnet_pos_import(mag_pos_fname)
b0_map_df = b0_map_import(b0_map_fname, B_unit='G')

b0_map_vals = b0_map_df.to_numpy()[:,3]
sensors = gen_sensors(b0_map_df)

if generate_shim:
    unshimmed_homogeneity = metric(b0_map_df.to_numpy()[:,3])/B0_nom*1e6
    print(f'Unshimmed Homogeneity: {unshimmed_homogeneity:.0f} ppm')

    # The idea of this placement algorithm is that each potential shim magnet 
    # position is checked at every possible rotation. If the rotation that has the
    # best resulting homogeneity is better than the present homogeneity, it is
    # added to the shim

    # The magnets are checked from the center ring working outwards, and within
    # each ring, the order in which the positions are checked is randomized

    magnet_pos = magnet_pos_df.to_numpy()[:,:3]
    n_magnets = magnet_pos.shape[0]

    # Initialize empty arrays of magnets to place and angles to place at
    best_placements = np.full(n_magnets,False)
    best_angles = np.zeros(n_magnets)

    # Generate center-out list of magnet offsets
    Xs = magnet_pos_df['X'].unique()
    Xs = sorted(Xs, key=abs)

    best_cost = unshimmed_homogeneity

    for p in range(n_passes):
        for X in Xs:
            print(f'X = {X}')
            ring_pos = magnet_pos_df[magnet_pos_df['X'] == X]
            # Shuffle magnets in ring
            ring_pos = ring_pos.sample(frac=1)
            
            # Iterate over locations in ring
            for index, row in ring_pos.iterrows():
                if best_placements[index]: # If there's already a magnet placed in that location
                    # Test all angles
                    test_angle = np.copy(best_angles)
                    angle_costs = np.zeros(n_angles)
                    for j in range(n_angles):
                        test_angle[index] = angles[j]
                        mag_pos_angle = np.concatenate((magnet_pos[best_placements,:], test_angle[best_placements, None]),1)
                        angle_costs[j] = compute_cost(mag_pos_angle, sensors, b0_map_vals)
                        # print(f'{magnet_pos[index,:]} @ {angles[j]:.2f}: {angle_costs[j]}')
                    lowest_cost_angle_index = np.argmin(angle_costs)
                    lowest_cost_angle = angles[lowest_cost_angle_index]
                    lowest_cost = angle_costs[lowest_cost_angle_index]

                    # If lowest cost placement is better than present placement, update angle
                    if lowest_cost < best_cost:
                        best_angles[index] = lowest_cost_angle
                        best_cost = lowest_cost
                        print(f'New Best Shim: {best_cost}')
                    # Test no placement
                    test_placement = np.copy(best_placements)
                    test_placement[index] = False
                    mag_pos_angle = np.concatenate((magnet_pos[best_placements,:], test_angle[best_placements, None]),1)
                    no_placement_cost =  compute_cost(mag_pos_angle, sensors, b0_map_vals)
                    
                    # if no placement is better than best placement, remove magnet
                    if no_placement_cost < best_cost:
                        best_placements[index] = False
                        best_angles[index] = 0
                        best_cost = no_placement_cost
                        print(f'Magnet {index} removed from shim. New Best Shim: {best_cost}')

                else:
                    test_placement = np.copy(best_placements)
                    test_placement[index] = True
                    test_angle = np.copy(best_angles)
                    angle_costs = np.zeros(n_angles)
                    for j in range(n_angles):
                        test_angle[index] = angles[j]
                        mag_pos_angle = np.concatenate((magnet_pos[test_placement,:], test_angle[test_placement, None]),1)
                        angle_costs[j] = compute_cost(mag_pos_angle, sensors, b0_map_vals)
                        # print(f'{magnet_pos[index,:]} @ {angles[j]:.2f}: {angle_costs[j]}')
                    lowest_cost_angle_index = np.argmin(angle_costs)
                    lowest_cost_angle = angles[lowest_cost_angle_index]
                    lowest_cost = angle_costs[lowest_cost_angle_index]
                    if lowest_cost < best_cost:
                        best_placements[index] = True
                        best_angles[index] = lowest_cost_angle
                        best_cost = lowest_cost
                        print(f'New Best Shim: {best_cost}')

    print("--- %s seconds ---" % (time.time() - start_time))

    # Save final shim
    with open(shim_out_fname, 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(['X', 'Y', 'Z', 'Place', 'Angle'])
        for i in range(n_magnets):
            writer.writerow([*magnet_pos[i,:], best_placements[i], best_angles[i]])

else:
    # Load shim
    shim = pd.read_csv(shim_out_fname, header=0)
    print(shim)
    magnet_pos = shim.to_numpy()[:,:3]
    best_placements = shim['Place'].to_numpy()
    best_angles = shim['Angle'].to_numpy()

# Analyze final shim
b0_map = b0_map_df.to_numpy()[:,3]
unshimmed_homogeneity_std = np.std(b0_map)/B0_nom*1e6
unshimmed_homogeneity_ptp = np.ptp(b0_map)/B0_nom*1e6

mag_pos_angle = np.concatenate((magnet_pos[best_placements,:], best_angles[best_placements, None]),1)
shim_map = compute_fields(mag_pos_angle, sensors)
b0_shimmed_z = shim_map[:,2]+b0_map
shimmed_homogeneity_std = np.std(b0_shimmed_z)/B0_nom*1e6
shimmed_homogeneity_ptp = np.ptp(b0_shimmed_z)/B0_nom*1e6

n_magnets_in_shim = best_placements.sum()
print(f'Final shim with {n_magnets_in_shim} magnets')

print(f'Unshimmed Homogeneity - Peak-to-peak: {unshimmed_homogeneity_ptp:.0f} ppm, Std Dev: {unshimmed_homogeneity_std} ppm')
print(f'Shimmed Homogeneity   - Peak-to-peak: {shimmed_homogeneity_ptp:.0f} ppm, Std Dev: {shimmed_homogeneity_std} ppm')

# f, ax = plt.subplots(1,2)
# Xs = b0_map_df.to_numpy()[:,0]
# Ys = b0_map_df.to_numpy()[:,1]
# Zs = b0_map_df.to_numpy()[:,2]
# ax[]
# # ax[0].scatter(Xs, Ys, Zs, c=b0_map)
# # ax[1].scatter(Xs, Ys, Zs, c=b0_shimmed_z)

magpy.show(generate_magnets(mag_pos_angle))

f, ax = plt.subplots(1,1)
ax.hist((b0_map, b0_shimmed_z), 20, label = ('Unshimmed', 'Shimmed'))
ax.legend()
ax.set_title('Reduced Set, Std Dev Minimized')
plt.show()