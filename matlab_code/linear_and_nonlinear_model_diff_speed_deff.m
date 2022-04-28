
delta_elevator_max_down = 15 * (pi/180); 
delta_elevator_max_up = -21 * (pi/180); 

theta_max_down = -6.0 * (pi/180); 
theta_max_up = 6.0 * (pi/180); 
Delta_H_target = 100;

model_names = ["nonlinear_model"];
delta_elevator_rate_down_array = [-15, -60]*(pi/180);
delta_elevator_rate_up_array = [15, 60]*(pi/180);

sim_time = 30;

for index_deff = 1:length(delta_elevator_rate_down_array)
    delta_elevator_rate_down = delta_elevator_rate_down_array(index_deff);
    delta_elevator_rate_up = delta_elevator_rate_up_array(index_deff);

    out = sim(model_names, sim_time);

    save_data_to_table(out.sim_omega_z, strcat("omega_z_DD_", num2str(delta_elevator_rate_up)), model_names, H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL_DIFF_SPEED)
    save_data_to_table(out.sim_Delta_H_target, strcat("Delta_H_target_DD_", num2str(delta_elevator_rate_up)), model_names, H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL_DIFF_SPEED)
    save_data_to_table(out.sim_delta_elevator, strcat("delta_elevator_DD_", num2str(delta_elevator_rate_up)), model_names, H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL_DIFF_SPEED)
    save_data_to_table(out.sim_theta, strcat("theta_DD_", num2str(delta_elevator_rate_up)), model_names, H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL_DIFF_SPEED)
    save_data_to_table(out.sim_Delta_H, strcat("Delta_H_DD_", num2str(delta_elevator_rate_up)), model_names, H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL_DIFF_SPEED)
    save_system_step_stats(out.sim_Delta_H, strcat("stats_DD_", num2str(delta_elevator_rate_up)), model_names, H_calc_bode(i), mach_calc_bode(i), FOLDER_MODEL_DIFF_SPEED);
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

function save_system_step_stats(param, param_name, model_name, H, mach, folder_path)
    save_name = create_sim_name(model_name, H, mach, param_name);
    step_info = stepinfo(param.Data, param.Time, 'SettlingTime', 0.05);
    writetable(struct2table(step_info), strcat(folder_path, save_name));
end
