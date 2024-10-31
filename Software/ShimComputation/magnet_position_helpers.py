"""Code to generate csvs for common shim magnet arrangements
All positions are in m, all angles in radians

Stephen Ogier - October 2024
"""
import csv
import numpy as np
from pathlib import Path

def make_csv(fname):
    """If file doesn't end in .csv, the extension will be changed to .csv
    """
    return Path(fname).with_suffix('.csv')

def cylinder(fname, magnets_per_ring, radius, x_offsets):
    """Magnets are arranged in rings around the X axis at specified offsets along X
    """

    angles = np.linspace(0, 2*np.pi, magnets_per_ring, endpoint=False)
    Ys = radius*np.sin(angles)
    Zs = radius*np.cos(angles)

    with open(make_csv(fname), 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(['X', 'Y', 'Z'])
        for x in x_offsets:
            Xs = np.full_like(Ys, x)
            rows = zip(Xs, Ys, Zs)
            writer.writerows(rows)

def cylinder_hallbach(fname, magnets_per_ring, radius, x_offsets):
    """Magnets are arranged in rings with Hallbach configuration around the X axis at specified offsets along X
    """

    angles = np.linspace(0, 2*np.pi, magnets_per_ring, endpoint=False)
    half_rot = np.linspace(0, 2*np.pi, int(magnets_per_ring/2), endpoint=False)
    rot = np.concatenate([half_rot, half_rot])
    Ys = radius*np.sin(angles)
    Zs = radius*np.cos(angles)

    with open(make_csv(fname), 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(['X', 'Y', 'Z', 'Rot'])
        for x in x_offsets:
            Xs = np.full_like(Ys, x)
            rows = zip(Xs, Ys, Zs, rot)
            writer.writerows(rows)

def OSII_MINI(fname):
    """Magnets arranged in rings based on the shim trays for the OSII MINI
    """
    radius = .076
    X_offsets = np.arange(-96,96+12,12)*1e-3
    angles = np.r_[-36:39+10:10, 54:174+10:10, 144:219+10:10, 234:309+10:10]/180*np.pi
    Ys = radius*np.sin(angles)
    Zs = radius*np.cos(angles)

    with open(make_csv(fname), 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(['X', 'Y', 'Z'])
        for x in X_offsets:
            Xs = np.full_like(Ys, x)
            rows = zip(Xs, Ys, Zs)
            writer.writerows(rows)


if __name__ == "__main__":
    OSII_MINI('OSII_MINI_reduced.csv')