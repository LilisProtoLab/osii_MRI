# System imports
import sys
import numpy as np
# Logging
import logging

# Local imports
from pyCoilGen.pyCoilGen_release import pyCoilGen
from pyCoilGen.sub_functions.constants import DEBUG_BASIC, DEBUG_VERBOSE

from os import makedirs

import matplotlib.pyplot as plt
from pyCoilGen.helpers.persistence import load
import pyCoilGen.plotting as pcg_plt


# Parameters
tikonov_factor = 6000
num_levels = 25
pcb_width = 0.002
cut_width = 0.01
normal_shift = 0.001
min_loop_significance = 2


normal_shift_smooth_factors = [5, 5, 5]

# From OSII project
circular_resolution = 10  # points on circle for conductor

conductor_radius = 0.0015 / 2
groove_depth = 0.005  # in meters

ratio_depth_width = (groove_depth - 2 * conductor_radius) / conductor_radius

# Generate cross-sectional points
angles1 = np.linspace(0, np.pi, circular_resolution)
angles2 = np.linspace(np.pi, 2 * np.pi, circular_resolution)
cross_sectional_points = np.array([
    -np.concatenate((np.sin(angles1), -ratio_depth_width + np.sin(angles2))),
    np.concatenate((np.cos(angles1), np.cos(angles2)))
])

cross_sectional_points = cross_sectional_points[:,-1::-1] # reverse the order of the points to make mesh face normals point outwards
cross_sectional_points *= conductor_radius

# Cylinder parameters
cylinder_height = 0.2-0.01 # remove one 0.5 cm on each side for as a margin 
cylinder_thickness = 0.004
# cylinder_radius = 0.071175
cylinder_radius = 0.071175 - cylinder_thickness + 0.001 + groove_depth / 2
# in meters (from CAD, limited by shimming structure radius 71.175, removing from that the thickness of the groove holder, adding 0.5mm for offset from wall, and adding the fact that cross-section is swept around the center of the cross-section)

if __name__ == '__main__':
    # Set up logging
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    # logging.basicConfig(level=logging.INFO)

    arg_dictZ = {
        'field_shape_function':'z', # definition of the target field
        'coil_mesh_file':'create cylinder mesh', 
        'cylinder_mesh_parameter_list': [cylinder_height, cylinder_radius,92, 42, 0, 1, 0, np.pi/2], # cylinder_height[in m], cylinder_radius[in m], num_circular_divisions,  num_longitudinal_divisions, rotation_vector: x,y,z, and  rotation_angle [radian]
        'surface_is_cylinder_flag':True, 
        'min_loop_significance': min_loop_significance,
        'target_region_radius':0.04,  # in meter
        'levels':num_levels,  # the number of potential steps that determines the later number of windings (Stream function discretization)
        'pot_offset_factor':0.5,  # a potential offset value for the minimal and maximal contour potential ; must be between 0 and 1
        'interconnection_cut_width':cut_width,  # the width for the interconnections are interconnected; in meter    
        'conductor_cross_section_width':pcb_width, #width of the generated pcb tracks
        #'normal_shift_length':normal_shift,  # the length for which overlapping return paths will be shifted along the surface normals; in meter
        'skip_postprocessing':False,
        'make_cylindrical_pcb':False,
        'skip_inductance_calculation':False,
        'cross_sectional_points':cross_sectional_points,
        'normal_shift_smooth_factors':normal_shift_smooth_factors,
        #'smooth_flag':True,
        'smooth_factor':2,
        'save_stl_flag':True,
        'tikhonov_reg_factor':tikonov_factor,
        'save_stl_flag': True,

        'output_directory': './projects/GradientCoils/final',  # [Current directory]
        'project_name': 'halbach_gradient_z',
        'persistence_dir': './projects/GradientCoils/final',
    }
    arg_dictY = {**arg_dictZ, 'field_shape_function': 'y', 'cylinder_mesh_parameter_list': [cylinder_height, cylinder_radius-cylinder_thickness,92, 42, 0, 1, 0, np.pi/2],'project_name': 'halbach_gradient_y',}

    arg_dictX = {**arg_dictZ, 'field_shape_function': 'x', 'cylinder_mesh_parameter_list': [cylinder_height, cylinder_radius-2*cylinder_thickness,92, 42, 0, 1, 0, np.pi/2,],'project_name': 'halbach_gradient_x',}


    #resultX = pyCoilGen(log, arg_dictX)
    #resultY = pyCoilGen(log, arg_dictY)
    resultZ = pyCoilGen(log, arg_dictZ)

    solution = resultY
    which = solution.input_args.project_name
    save_dir = f'{solution.input_args.output_directory}'
    makedirs(save_dir, exist_ok=True)

    coil_solutions = [solution]

    # Plot a multi-plot summary of the solution
    pcg_plt.plot_various_error_metrics(coil_solutions, 0, f'{which}', save_dir=save_dir)

    # Plot the 2D projection of stream function contour loops.
    pcg_plt.plot_2D_contours_with_sf(coil_solutions, 0, f'{which} 2D', save_dir=save_dir)
    pcg_plt.plot_3D_contours_with_sf(coil_solutions, 0, f'{which} 3D', save_dir=save_dir)

    # Plot the vector fields
    coords = solution.target_field.coords

    # Plot the computed target field.
    plot_title = f'{which} Target Field '
    field = solution.solution_errors.combined_field_layout
    pcg_plt.plot_vector_field_xy(coords, field, plot_title=plot_title, save_dir=save_dir)

    # Plot the difference between the computed target field and the input target field.
    plot_title = f'{which} Target Field Error '
    field = solution.solution_errors.combined_field_layout - solution.target_field.b
    pcg_plt.plot_vector_field_xy(coords, field, plot_title=plot_title, save_dir=save_dir)