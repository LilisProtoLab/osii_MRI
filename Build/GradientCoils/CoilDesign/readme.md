# CoilDesign

## 📋 Table of Contents

- [CoilDesign](#coildesign)
  - [📋 Table of Contents](#-table-of-contents)
  - [🚀 Getting Started](#-getting-started)
  - [📁 Folder Structure](#-folder-structure)
  - [🛠️ Usage](#️-usage)
    - [MATLAB Version](#matlab-version)
    - [Python Version](#python-version)
  - [🏭 Manufacturing Process](#-manufacturing-process)
  - [📊 Coil Characteristics](#-coil-characteristics)
  - [📐 Parameters in Present Implementation](#-parameters-in-present-implementation)
    - [Physical Constraints](#physical-constraints)
    - [Design Parameters](#design-parameters)
  - [💡 Remarks on the Design](#-remarks-on-the-design)

## 🚀 Getting Started

Follow these instructions to set up and run the coil design scripts.

## 📁 Folder Structure

```bash
CoilDesign/
├── Print/                   # Contains Fusion360 file and STL files for printing final coils
├── Prototype/               # Design files for mini prototype coil
├── src/                     # Source code for coil design
└── readme.md                # Main readme file for CoilDesign
```

## 🛠️ Usage

The two files in [src](src/) generate a number of output files. The output files also include .stl files containing the wire path for the coil. To be more precise the output .stl files contain a mesh which can be seen as a groove which can be cut into a cylinder to act as a holder for a gradient coil.

### MATLAB Version

1. Ensure [CoilGen](https://github.com/Philipp-MR/CoilGen/tree/main) is downloaded
2. In `generate_gradients.m` set the path to your downloaded [CoilGen](https://github.com/Philipp-MR/CoilGen/tree/main) folder and set parameters for your coil design
3. Run the script to generate coil design

### Python Version

1. Install [PyCoilGen](https://pycoilgen.readthedocs.io/en/stable/)
2. If needed, configure parameters in `generate_gradients.py`
3. Run the script to generate coil designs
4. You will get .stl files which you can use for manufacturing

For more details about the code, look in the [src](src/) folder

## 🏭 Manufacturing Process

The created .stl files containing the wire path were imported into Autodesk Fusion. There, the wire path was subtracted from a cylinder, which created the coil holders. This resulting mesh was used for the 3D prints. For details on the manufacturing of the coil holders, look in the [Print](Print/) folder.

## 📊 Coil Characteristics

|                     | Z Gradient           | Y Gradient | X Gradient |
| ------------------- | -------------------- | ---------- | ---------- |
| Efficiency (mT/m/A) | 1.9698 (measured ~2) | 3.1017     | 1.4213     |
| Resistance (mOhm)   | 255 (measured 269)   | 273        | 220        |
| Inductance (μH)     | 78.1                 | 85.0       | 48.0       |
| Radius (cm)         | 7.07                 | 6.67       | 6.27       |
| Wire length (m)     | 17.9                 | 19.1       | 15.4       |

## 📐 Parameters in Present Implementation

### Physical Constraints

- Available space: radius 71.175 mm, length 200 mm
- Wire thickness: 1.25 mm (diameter)

### Design Parameters

- Cylinder height: 190 mm (200 mm - 10 mm margin)
- Cylinder thickness: 4 mm
- Groove depth: 5 mm (the "elongation" of the wire path in radial direction in order to create a groove which can be subtracted from the cylinder)
- Conductor radius: 0.75 mm (0.25 mm thicker than actual wire yielded good results in our prints)
- Tikhonov factor: 6000 (optimal values can be found out by a parameter sweep. An example file on how to sweep over parameters can be found in the [PyCoilGen](https://github.com/kev-m/pyCoilGen/blob/master/examples/halbach_gradient_x.py) repository)
- Smooth factor: 2-3 (coil dependent)

## 💡 Remarks on the Design

After talking with an expert in the field, we were told that y and z gradient coils can have the same design (one that resembles our y gradient), but with a 45° rotation. Our z-gradient might have a lower linear error than the aforementioned configuration; however, their efficiency is lower. Furthermore, the same expert explained that it is possible to design the y and z gradients "by hand," by using the fact that we want a linear gradient in a field perpendicular to a cylinder's direction. That leads to a wire distribution which follows an arcsin for each 90° of the cylinder (the current density and thus the wire spacing have to follow an arcsin). For an infinitely long cylinder, that would be the perfect configuration. For a finite cylinder, the ends of the wires need to be connected to loops. The deviation from straight wires along the cylinder axis in our y gradient reduces the error only by a few percent according to the mentioned expert.
