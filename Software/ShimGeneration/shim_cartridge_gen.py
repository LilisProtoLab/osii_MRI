"""Code to generate shim cartridges for OSII Mini from computed shims

Resulting shim cartridges are named prefix[ABCD][Slot #], where:
the A cartridge is centered on the +Z axis, B along +Y, C along -Z, and D along -Y
# indicates the number of slot, moving from -X to +X. If a reduced set of slots is
being used, unused slots are NOT counted

Note: The shim definition files are in m, while the CAD is all in mm.
"""
import pandas as pd
import cadquery as cq
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
# set_port(3939)
import numpy as np

# Files that need to be defined
shim_file = '../ShimComputation/NIST_Shim_reduced_ptp_3.csv'
cartridge_template_file = 'shim_cartridge_V3.stp'
cartridge_prefix = 'reduced_ptp_3_'

cartridge_blank = cq.importers.importStep(cartridge_template_file)

# Rotate cartridge_blank to optimal position to add text
cartridge_blank = cartridge_blank.rotate((0,0,0),(0,1,0),90).rotate((0,0,0),(0,1,0),180)

# Define magnet hole, with notch in +Z direction
s = 1.55 # Magnet side half-length
magnet_hole = (
    cq.Workplane('YZ')
    .sketch()
    .segment((s,s),(s,.75))
    .segment((s+.75,0))
    .segment((s,-.75))
    .segment((s,-1*s))
    .segment((-1*s,-1*s))
    .segment((-1*s,1*s))
    .close()
    .assemble(tag="face")
    .finalize()
    .extrude(-3)
    .rotate((0,0,0),(1,0,0),90)
    )

def gen_cartridge(magnet_row_df, row, sector):
    """Generate a shim cartridge for a given row and sector
    """
    if len(magnet_row_df) == 0:
        return
    
    cartridge = cartridge_blank

    # Add embossed label text to cartridge
    cartridge = (cartridge
                .faces("<X")
                .workplane()
                .center((77)*np.sin(85*np.pi/180),(77)*np.cos(85*np.pi/180))
                .text(f"{sector}{row}",3,-.5, kind='bold')
                )
    
    if sector == 'A':
        cartridge = cartridge.rotate((0,0,0),(1,0,0),-45)
    elif sector == 'B':
        cartridge = cartridge.rotate((0,0,0),(1,0,0),-135)
    elif sector == 'C':
        cartridge = cartridge.rotate((0,0,0),(1,0,0),135)
    else:
        cartridge = cartridge.rotate((0,0,0),(1,0,0),45)
    
    for index, magnet in magnet_row_df.iterrows():
        Y = magnet['Y']*1e3 # Convert to mm
        Z = magnet['Z']*1e3 # Convert to mm
        angle = magnet['Angle']*180/np.pi
        print(f'Magnet at {Y:.3f},{Z:.3f} aka {magnet["Loc Angle"]:.0f}')
        magnet_sub = magnet_hole.rotate((0,0,0),(1,0,0),angle).translate((0,Y,Z))
        cartridge = cartridge - magnet_sub
    # show(cartridge)
    # input()
    cartridge.export(f'{cartridge_prefix}{sector}{row}.stl')
        

shim_df = pd.read_csv(shim_file)
# Add column for location angle
shim_df['Loc Angle'] = np.arctan2(shim_df['Y'], shim_df['Z'])*180/np.pi

# Get unique offsets
Xs = shim_df['X'].unique()

# Filter only populated positions
shim_df = shim_df[shim_df['Place']]

# Iterate over rows in shim tray, generating cartridges
for row, X in enumerate(Xs):
    row_df = shim_df[shim_df['X'] == X]
    row_A_df = row_df[(row_df['Loc Angle'] > -45) & (row_df['Loc Angle']  < 45)]
    row_B_df = row_df[(row_df['Loc Angle'] > 45) & (row_df['Loc Angle']  < 135)]
    row_D_df = row_df[(row_df['Loc Angle'] < -45) & (row_df['Loc Angle']  > -135)]
    row_C_df = row_df[(row_df['Loc Angle'] > 135) | (row_df['Loc Angle']  < -135)]
    gen_cartridge(row_A_df,row,'A')
    gen_cartridge(row_B_df,row,'B')
    gen_cartridge(row_C_df,row,'C')
    gen_cartridge(row_D_df,row,'D')
    