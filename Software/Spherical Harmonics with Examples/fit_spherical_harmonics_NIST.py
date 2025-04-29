# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:10:27 2024

@author: to_reilly

Modified for NIST use by Stephen Ogier September 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm
from scipy.linalg import lstsq
import csv

b0_map_fname = r'NIST_Smallbach_Swap_Centered.csv'

#The highest order spherical harmonic to fit
maxOrder = 15

def cartToSpher(coords):
    r = np.sqrt(np.sum(np.square(coords),axis = -1))    
    #remove r = 0 to avoid divide by zero
    r[r==0] = np.nan
    
    phi = np.arctan2(coords[...,1], coords[...,0]) + np.pi
    theta = np.arccos(coords[...,2]/r)
    return np.stack([r,theta, phi], axis = -1)

def getRealSphericalHarmonics(coords, maxOrder):
    r0          = np.nanmean(coords[...,0])       #Get the mean radius for normalisation
    print(r0)
    spherHarm   = np.zeros((np.shape(coords[...,0]) + ((maxOrder + 1)**2,)))
    idx         = 0
    for n in range(maxOrder+1):
        for m in range(-n,n+1):
            if m < 0:
                spherHarm[...,idx] = ((1j/np.sqrt(2))*(np.divide(coords[...,0],r0)**n)*(sph_harm(m,n,coords[...,2], coords[...,1])-((-1)**m)*sph_harm(-m,n,coords[...,2], coords[...,1]))).real
            elif m > 0:
                spherHarm[...,idx] = ((1/np.sqrt(2))*(np.divide(coords[...,0],r0)**n)*(sph_harm(-m,n,coords[...,2], coords[...,1])+((-1)**m)*sph_harm(m,n,coords[...,2], coords[...,1]))).real
            elif m == 0:
                spherHarm[...,idx] = np.multiply(sph_harm(m,n,coords[...,2], coords[...,1]),np.divide(coords[...,0],r0)**n).real
            else:
                print("That wasnt suppoosed to happen!")
            idx += 1
    return spherHarm

rawData = np.genfromtxt(b0_map_fname, dtype = float, delimiter = ',', skip_header = 1)[:,:4]

radius = np.sqrt(np.mean(np.square(rawData[:,0]) + np.square(rawData[:,1]) + np.square(rawData[:,2])))
fieldAxis = 3

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(rawData[:,0], rawData[:,1], rawData[:,2], c = rawData[:,3], cmap = 'viridis')
# ax.set_xlabel("X [mm] Bore direction")
# ax.set_ylabel("Y [mm] (up down)")
# ax.set_zlabel("Z [mm] (B0)")
# fig.suptitle("Raw data - Radius %.2f mm"%(radius))

shifted_data = np.copy(rawData)

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(shifted_data[:,0], shifted_data[:,1], shifted_data[:,2], c = shifted_data[:,3], cmap = 'viridis')
# ax.set_xlabel("X [mm] Bore direction")
# ax.set_ylabel("Y [mm] (up down)")
# ax.set_zlabel("Z [mm] (B0)")
# fig.suptitle("Re-oriented")

spher_coords = cartToSpher(shifted_data[:,:3])
spherHarm = getRealSphericalHarmonics(spher_coords, maxOrder)

initialGuess = np.zeros((np.size(spherHarm,-1)))

np.savetxt('spherHarm.csv', spherHarm, delimiter=',')

plt.figure()
plt.plot(rawData[:,fieldAxis])
lsqFit = lstsq(spherHarm, rawData[:,fieldAxis])
spherHarmCoeff = lsqFit[0]

relative = np.max(np.abs(spherHarmCoeff[1:]))/spherHarmCoeff[0]
print(f'Relative strength of strongest non-B0 Spherical Harmonic: {relative}')

plt.figure()
plt.plot(spherHarmCoeff[1:])
plt.title("Spherical harmonic coefficients")

fittedData = np.matmul(spherHarm, spherHarmCoeff)
print(f'spherHarm:      {spherHarm.shape}')
print(f'spherHarmCoeff: {spherHarmCoeff.shape}')
print(f'fittedData:     {fittedData.shape}')
print(f'shifted_data:   {shifted_data.shape}')


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(shifted_data[:,0], shifted_data[:,1], shifted_data[:,2], c = fittedData, cmap = 'viridis')
ax.set_xlabel("X [mm] Bore direction")
ax.set_ylabel("Y [mm] (up down)")
ax.set_zlabel("Z [mm] (B0)")
fig.suptitle('Fitted data')
# plt.show()

spherical_harm_fname = r'NIST_spherical_harmonic_coefficients'
np.save(spherical_harm_fname, spherHarmCoeff)

# Save smoothed pherical harmonics
smoothed_map_fname = r'NIST_Smallbach_Swap_Smoothed.csv'
with open(smoothed_map_fname, 'w', newline='') as f:
    print(smoothed_map_fname)
    writer = csv.writer(f, dialect='excel')
    writer.writerow(['X', 'Y', 'Z', 'B0'])
    for i in range(len(fittedData)):
        writer.writerow([*shifted_data[i,:3], fittedData[i]])
