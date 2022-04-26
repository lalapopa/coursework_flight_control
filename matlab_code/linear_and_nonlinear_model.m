delta_elevator_max_down = 15 * (pi/180); 
delta_elevator_max_up = -21 * (pi/180); 

delta_elevator_rate_down = -24 * (pi/180);
delta_elevator_rate_up = 24 * (pi/180);

theta_max_down = -6.0 * (pi/180); 
theta_max_up = 6.0 * (pi/180); 
Delta_H_target = 100;

model_names = ["linear_model", "nonlinear_model"];
sim_time = 30;

for model_name_index = 1:length(model_names)
    out = sim(model_names(model_name_index), sim_time);

    save_data_to_table(out.sim_omega_z, "omega_z", model_names(model_name_index), H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL)
    save_data_to_table(out.sim_Delta_H_target, "Delta_H_target", model_names(model_name_index), H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL)
    save_data_to_table(out.sim_delta_elevator, "delta_elevator", model_names(model_name_index), H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL)
    save_data_to_table(out.sim_theta, "theta", model_names(model_name_index), H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL)
    save_data_to_table(out.sim_Delta_H, "Delta_H", model_names(model_name_index), H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL)
end

function save_data_to_table(param, param_name, model_name, H, mach, folder_path) 
    ready_table = table(param.Time, param.Data);
    ready_table.Properties.VariableNames = {'time' 'value'};

    save_name = create_sim_name(model_name, H, mach, param_name);
    save_path = strcat(folder_path, save_name);
    writetable(ready_table, save_path, 'Delimiter', ',');
end

function out = get_var_name(var)
    out = inputname(1);
end

function name = create_sim_name(model_type, H, mach, param)
    name = string(sprintf('%s_%s_H_%i_M_0_%4.0f.csv', model_type, param, H, mach*10000));
end








