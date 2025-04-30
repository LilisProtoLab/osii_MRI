# Print

## Used software/hardware

- Autodesk fusion 360
- PrusaXL
  - PLA and PETG as filaments
- copper wire
- flat screw driver

## Manufacturing

After designing the coils in (py)CoilGen and having the .stl files with the wire pattern the print can be prepared.

Here is a step by step guide on how we proceeded:

1. **Design coil holders in Autodesk Fusion**
   1. create cylinders with corresponding geometry for the coils
   2. convert cylinders to mesh files
   3. import .stl files from coilgen and pycoilgen
   4. subtract imported wirepaths from cylinders
   5. export meshes

    Our design can be opened by uploading [this file](./CoilDesign%20v1.f3z) to the Fusion workspace.

2. **3D printing:**
   We printed our coil holders on a PrusaXL.
   We used PLA as structural material and PETG as support with organic support in the Prusa slicer (see Prusa [project file](xCoil.3mf)). This ensured that the support did not adhere to the structure and was easier to remove by the organic support around the structure.
   We have also tried PVA as support material, however, had difficulties with clogged nozzles or chunks of PVA accumulating on the print which were then hit by the printhead such that the whole print moved.

3. **Putting Wire into coil holder:**
   In our case the pressfit for the copper wire in the coil holders was quite tight. We used a flathead screwdriver which we covered with heat shrink tubing in order to not scratch the coating of the wire. We assume that covering the tip of the screw driver with some epoxy might work better as we had to change the shrinking tubing often because of holes.
