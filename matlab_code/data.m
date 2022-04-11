mach = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8];
plane.bar_x_t = 0.45;
plane.I_z = 19*10^6;
plane.S = 300;
plane.b_a = 7.5;
plane.m = 140000;

%%%%%%%%%%%%%%%%%%%%%%
%  READ FLIGHT AREA  %
%%%%%%%%%%%%%%%%%%%%%%

file_name = "../data/table_2.csv";
opts = detectImportOptions(file_name);
opts.SelectedVariableNames = [1,5,6,11]; 
csv_data = readmatrix(file_name, opts); 

H_array = csv_data(:, 1) * 1000;
M_min = csv_data(:, 2); 
M_max = csv_data(:, 3); 
M_lf = csv_data(:, 4); 
calc_mach = [M_min M_lf M_max];
to_delete = {'file_name','opts','csv_data', 'vars'};
clear(to_delete{:});


