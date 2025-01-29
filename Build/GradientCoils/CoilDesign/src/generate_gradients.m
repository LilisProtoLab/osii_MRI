
%This script generates a cylindrical "z" gradient coil for a halbach i.e.
%the cylinder rotated for 90deg
%% modified version
% this script is a combination of generate_halbach_gradient_system from the CoilGen repository and Linear_GradientCoil from the OSII repository
%%

clc; clear all;
addpath(genpath('../CoilGen/')); % add the path to the CoilGen repository

tikonov_factor=6000;
num_levels=25;  % the number of potential steps that determines the later number of windings (Stream function discretization)
cut_width=0.01; % the width for the interconnections are interconnected; in meter
normal_shift=0.001; % the length for which overlapping return paths will be shifted along the surface normals; in meter
min_loop_signifcance=2; % the minimal significance of a loop to be considered in the optimization

normal_shift_smooth_factors=[3 3 3];

%% from OSII project
circular_resolution=10; % points on circle for conductor

conductor_radius= 0.0015/2;
groove_depth = 0.005;       % in m


ratio_depth_width = (groove_depth-2*conductor_radius)/conductor_radius;

cross_sectional_points = -[sin(0:(2*pi)/(circular_resolution-1):pi),-ratio_depth_width+sin(pi:(2*pi)/(circular_resolution-1):2*pi); cos(0:(2*pi)/(circular_resolution-1):pi),cos(pi:(2*pi)/(circular_resolution-1):2*pi)];
cross_sectional_points = [cross_sectional_points cross_sectional_points(:,1)];
cross_sectional_points=cross_sectional_points.*repmat(conductor_radius,[2 1]);


cylinder_heigth = 0.2-0.01;

cylinder_thickness = 0.004;
 
cylinder_radius = 0.071175-(cylinder_thickness)+0.001+groove_depth/2; % in m ( limited by shimming structure radius 71.175, removing from that the thickness of the groove holder, adding 0.5mm for offset from wall, and adding the fact that crossection is sweepeed around center of crossection)
figure
plot(cross_sectional_points(1,:),cross_sectional_points(2,:))
axis equal

%% Run the algorithm
%try
zParams = struct(...
    'field_shape_function','z',... % definition of the target field
    'coil_mesh_file','create cylinder mesh', ...
    'cylinder_mesh_parameter_list',[cylinder_heigth cylinder_radius 92 42 0 1 0 pi/2],... % cylinder_height[in m], cylinder_radius[in m], num_circular_divisions,  num_longitudinal_divisions, rotation_vector: x,y,z, and  rotation_angle [radian]
    'surface_is_cylinder_flag',true, ...
    'min_loop_signifcance',min_loop_signifcance,...
    'skip_normal_shift',false,...
    'target_region_radius',0.04,...  % in meter
    'levels',num_levels, ... % the number of potential steps that determines the later number of windings (Stream function discretization)
    'pot_offset_factor',0.5, ... % a potential offset value for the minimal and maximal contour potential ; must be between 0 and 1
    'interconnection_cut_width',cut_width, ... % the width for the interconnections are interconnected; in meter    'conductor_cross_section_width',pcb_width,... %width of the generated pcb tracks 
    'normal_shift_length',normal_shift, ... % the length for which overlapping return paths will be shifted along the surface normals; in meter
    'skip_postprocessing',false,...
    'skip_inductance_calculation',true,...
    'make_cylndrical_pcb',false,...
    'cross_sectional_points',cross_sectional_points,...    
    'normal_shift_smooth_factors',normal_shift_smooth_factors,...    %'smooth_flag',true,...    %'smooth_factor',2,...
    'save_stl_flag',true,...
    'tikonov_reg_factor',tikonov_factor); %Tikonov regularization factor for the SF optimization

yParams = zParams;
yParams.field_shape_function = 'y';
yParams.cylinder_mesh_parameter_list=[cylinder_heigth cylinder_radius-cylinder_thickness 92 42 0 1 0 pi/2];

xParams = zParams;
xParams.field_shape_function = 'x';
xParams.cylinder_mesh_parameter_list=[cylinder_heigth cylinder_radius-2*cylinder_thickness 92 42 0 1 0 pi/2];



%coil_x.out=CoilGen(xParams);

%coil_y.out=CoilGen(yParams);

coil_z.out=CoilGen(zParams);
%%save('Parameters.mat')
%% Plot results
close all;

coil_name='Coil';

coils_to_plot=coil_z;

% if ispc
% addpath(strcat(pwd,'\','plotting'));
% else
% addpath(strcat(pwd,'/','plotting'));
% end
%Chose a even leveled solution for plotting
%solutions_to_plot=find(arrayfun(@(x) ~isempty(coils_to_plot),1:numel(coil_layouts)));
single_ind_to_plot= find_even_leveled_solution(coils_to_plot);
plot_error_different_solutions(coils_to_plot,single_ind_to_plot,coil_name);
plot_2D_contours_with_sf(coils_to_plot,single_ind_to_plot,coil_name);
plot_3D_sf(coils_to_plot,single_ind_to_plot,coil_name);
plot_groups_and_interconnections(coils_to_plot,single_ind_to_plot,coil_name);
plot_coil_parameters(coils_to_plot,coil_name);
plot_coil_track_with_resulting_bfield(coils_to_plot,single_ind_to_plot,coil_name);
plot_various_error_metrics(coils_to_plot,single_ind_to_plot,coil_name);
plot_resulting_gradient(coils_to_plot,single_ind_to_plot,coil_name);

plot_pcb_layouts(coils_to_plot,single_ind_to_plot,coil_name);

%rmpath('plotting');

