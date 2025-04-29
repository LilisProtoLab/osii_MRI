# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:10:27 2024

@author: to_reilly
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm
from scipy.linalg import lstsq

def cartToSpher(coords):
    r = np.sqrt(np.sum(np.square(coords),axis = -1))    
    #remove r = 0 to avoid divide by zero
    r[r==0] = np.nan
    
    phi = np.arctan2(coords[...,1], coords[...,0]) + np.pi
    theta = np.arccos(coords[...,2]/r)
    return np.stack([r,theta, phi], axis = -1)

def getRealSphericalHarmonics(coords, maxOrder):
    r0          = np.nanmean(coords[...,0])       #Get the mean radius for normalisation
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


# def fitSphericalHarmonics(fitVector, args):
#     return np.square(maskedFieldShell - np.matmul(spherHarm, fitVector))


# filename = r'/Users/tom/Dropbox/Low field data/OSII One/Field maps/Paraguay/Initial field map.csv' 
# rawData = np.genfromtxt(filename, dtype = float, delimiter = ',', skip_header = 1)[:,2:]

filename = r'output_1-6_data.csv'
# 
rawData = np.genfromtxt(filename, dtype = float, delimiter = ',', skip_header = 1)


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
shifted_data[:,1] *= -1 #invert y axis

# temp = np.copy(shifted_data[:,1])
# shifted_data[:,1] = shifted_data[:,2]
# shifted_data[:,2] = temp
# shifted_data[:,2] *= -1

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(shifted_data[:,0], shifted_data[:,1], shifted_data[:,2], c = shifted_data[:,3], cmap = 'viridis')
# ax.set_xlabel("X [mm] Bore direction")
# ax.set_ylabel("Y [mm] (up down)")
# ax.set_zlabel("Z [mm] (B0)")
# fig.suptitle("Re-oriented")


#The highest order spherical harmonic to fit
maxOrder = 15


spher_coords = cartToSpher(shifted_data[:,:3])
spherHarm = getRealSphericalHarmonics(spher_coords, maxOrder)

initialGuess = np.zeros((np.size(spherHarm,-1)))

np.savetxt('spherHarm_PY.csv', spherHarm, delimiter=',')

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

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(shifted_data[:,0], shifted_data[:,1], shifted_data[:,2], c = fittedData, cmap = 'viridis')
ax.set_xlabel("X [mm] Bore direction")
ax.set_ylabel("Y [mm] (up down)")
ax.set_zlabel("Z [mm] (B0)")
fig.suptitle('Fitted data')
plt.show()
filename = r'RDPY_Shim check - Shims 1 to 6 - Interp.npy'

print(spherHarmCoeff)
np.save(filename, spherHarmCoeff)

# filename = r'/Users/tom/Dropbox/Low field data/OSII One/Field maps/Paraguay/Initial map - Interp - 5 mm res, 250mm DSV.npy'


# interpolated_data = np.load(filename)

# x = np.linspace(-125,125,np.size(interpolated_data,0),endpoint=True)
# x = np.linspace(0,250,np.size(interpolated_data,0),endpoint=True)

# xDim, yDim, zDim = np.meshgrid(x,x,x, indexing = 'xy')

# mask = ~(np.isnan(interpolated_data))

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(xDim[mask], yDim[mask], zDim[mask], c = interpolated_data[mask], cmap = 'viridis')
# ax.set_xlabel("X [mm] Bore direction")
# ax.set_ylabel("Y [mm] (up down)")
# ax.set_zlabel("Z [mm] (B0)")

# outputFile = r'Initial map.path'

# with open(outputFile,'w') as file:
#     maskedX = xDim[mask]
#     maskedY = yDim[mask]
#     maskedZ = zDim[mask]
#     for idx in range(np.size(maskedX)):
#         file.write("X%dY%dZ%d\n"%(maskedX[idx], maskedY[idx],maskedZ[idx]))
        
# outputFile = r'Initial map.txt'

# with open(outputFile,'w') as file:
#     fieldData = interpolated_data[mask]/10
#     for idx in range(np.size(fieldData)):
#         file.write("%f\n"%(fieldData[idx]))
