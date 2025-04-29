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
shim_fname = 'NYU_Shim_reduced_ptp_3.csv'
b0_map_fname = 'example_data/background_removed_2024_05_07_b0_sphere_100mm_5mm_increment.csv'
shim_map_fname = 'NYU_Shim_reduced_ptp_3_map.csv'
b0_map_export_fname = 'NYU_full_b0_map.csv'
# If True, generate shim. If false, attempt to load existing shim from shim_out_fname
generate_shim = True

# Choose cost function
# ptp - minimize max(B0)-min(B0)
# std - minimize std(B0)
cost_fn = 'std'

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
    B_shim = magnets.getB(sensors)

    return B_shim

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

b0_map_df = b0_map_import(b0_map_fname, B_unit='G')

b0_map_XYZ = b0_map_df.to_numpy()[:,:3]
b0_map_vals = b0_map_df.to_numpy()[:,3]
sensors = gen_sensors(b0_map_df)

# Load shim
shim = pd.read_csv(shim_fname, header=0)
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

print(f'Unshimmed Homogeneity - Peak-to-peak: {unshimmed_homogeneity_ptp:.0f} ppm, Std Dev: {unshimmed_homogeneity_std} ppm')
print(f'Shimmed Homogeneity   - Peak-to-peak: {shimmed_homogeneity_ptp:.0f} ppm, Std Dev: {shimmed_homogeneity_std} ppm')

with open(shim_map_fname, 'w', newline='') as f:
    print(shim_map_fname)
    writer = csv.writer(f, dialect='excel')
    writer.writerow(['X', 'Y', 'Z', 'B0'])
    for i in range(len(b0_shimmed_z)):
        writer.writerow([*b0_map_XYZ[i,:3], b0_shimmed_z[i]])

with open(b0_map_export_fname, 'w', newline='') as f:
    print(b0_map_export_fname)
    writer = csv.writer(f, dialect='excel')
    writer.writerow(['X', 'Y', 'Z', 'B0'])
    for i in range(len(b0_map)):
        writer.writerow([*b0_map_XYZ[i,:3], b0_map[i]])

fig = plt.figure()
ax1 = fig.add_subplot(1,2,1, projection='3d')
ax2 = fig.add_subplot(1,2,2, projection='3d')
Xs = b0_map_df.to_numpy()[:,0]
Ys = b0_map_df.to_numpy()[:,1]
Zs = b0_map_df.to_numpy()[:,2]
ax1.scatter(Xs, Ys, Zs, c=b0_map, marker='o')
ax2.scatter(Xs, Ys, Zs, c=b0_shimmed_z, marker='o') 
# ax[1].scatter(Xs, Ys, Zs, c=b0_shimmed_z, marker='o')
plt.show()