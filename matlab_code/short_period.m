clear;
run('data.m');
run('omega_0_max_xi_s_max_find.m');
FOLDER = '~/Documents/uni/4_course/2_sem/flight_control/cource_work/code/data/';
aero_data = AeroDynamicsData;

p = tf('p');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Servo motor parameters  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

T_n_theory = 1/(10*omega_0_max);
T_n_allowed = [0.02 0.025 0.003 0.035 0.04 0.045 0.05];
T_n = find_closest_value_in_array(T_n_allowed, T_n_theory);
xi_n = 0.7;
W_p = 1/(T_n^2*p^2 + 2*xi_n*T_n*p + 1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  FIND K_omega_z K_theta  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%calc_mach = increase_column_elements(calc_mach, 10);
[r, c] = size(calc_mach);

K_omega_z = zeros(r, c);
K_theta = zeros(r, c);
K_H = zeros(r, c);
i_H = zeros(r, c);
V = zeros(r, c);
q = zeros(r, c);


[epsilon, nu] = epsilon_nu_find(mach_calc_xi, H_calc_xi, aero_data, plane, W_p, T_n, 0.25, omega_0_max, omega_0_max);
disp(['epsilon= ', num2str(epsilon), 'nu= ', num2str(nu)]);

for i = 1:r 
    for j = 1:c
        [m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(calc_mach(i,j), H_array(i), aero_data, plane);
        [~, a, ~, rho] = atmosisa(H_array(i));

        V(i, j) = calc_mach(i, j).*a;
        q(i, j) = (rho.*V(i,j).^2)/2;
        T_1c = 1/bar_Y_alpha;
        K_omega_z_gr = -(1/(bar_M_z_delta_v*T_n));
        K_omega_z(i, j) = epsilon*K_omega_z_gr;
        K_theta(i, j) = nu*K_omega_z(i,j);
        K_H(i, j) = V(i, j);
        i_H(i, j) = 0.8*(1/(T_1c*V(i,j)));
    end
end

[K_omega_z_calc, q_calc] = get_trend_approx_values(K_omega_z, q, max(size(calc_mach)));
K_theta_calc = get_trend_approx_values(K_theta, q, max(size(calc_mach)));

csvwrite([FOLDER 'K_H_all.csv'], K_H);
csvwrite([FOLDER 'K_omega_z_all.csv'], K_omega_z);
csvwrite([FOLDER 'K_theta_all.csv'], K_theta);
csvwrite([FOLDER 'q_all.csv'], q);
csvwrite([FOLDER 'H_all.csv'], H_array);
csvwrite([FOLDER 'omega_0_pr.csv'], omega_0_H_M);
csvwrite([FOLDER 'xi_s_all.csv'], xi_s_H_M);
csvwrite([FOLDER 'fine_K_omega_z.csv'], K_omega_z_calc);
csvwrite([FOLDER 'fine_K_theta.csv'], K_theta_calc);
csvwrite([FOLDER 'fine_q.csv'], q_calc);

%%%%%%%%%%%%%%%%%%%%
%  A/P alt design  %
%%%%%%%%%%%%%%%%%%%%
H_calc = 10000; % Level flight
mach_calc = return_element_in_another_matrix(H_array, H_calc, calc_mach);
[r, c] = size(mach_calc);

for i = 1:c
    K_omega_z_int = get_K_value(K_omega_z_calc, q_calc, mach_calc(i), H_calc);
    K_theta_int = get_K_value(K_theta_calc, q_calc, mach_calc(i), H_calc);

    [W_AP_theta, W_AP_alt, W_AP_theta_ol, W_AP_alt_ol] = get_control_system(mach_calc(i), H_calc, K_omega_z_int, K_theta_int,...
        aero_data, plane, W_p);
    
    W_t_latex = tf_to_latex(W_AP_theta, 3)
    W_a_ol_latex = tf_to_latex(W_AP_alt_ol, 3)
    W_a_latex = tf_to_latex(W_AP_alt, 3)
    W_t_ol_latex = tf_to_latex(W_AP_theta_ol, 3)
    
    data_names = [
        string(sprintf('W_theta_ol_H_%i_M_0_%4.0f', H_calc, mach_calc(i)*10000)),...
        string(sprintf('W_theta_H_%i_M_0_%4.0f', H_calc, mach_calc(i)*10000)),...
        string(sprintf('W_altitude_H_%i_M_0_%4.0f', H_calc, mach_calc(i)*10000)),...
        string(sprintf('W_altitude_ol_H_%i_M_0_%4.0f', H_calc, mach_calc(i)*10000)),...
        ];
    data_names_bode_stats = [
        string(sprintf('W_theta_ol_H_%i_M_0_%4.0f_stats', H_calc, mach_calc(i)*10000)),...
        string(sprintf('W_theta_H_%i_M_0_%4.0f_stats', H_calc, mach_calc(i)*10000)),...
        string(sprintf('W_altitude_H_%i_M_0_%4.0f_stats', H_calc, mach_calc(i)*10000)),...
        string(sprintf('W_altitude_ol_H_%i_M_0_%4.0f_stats', H_calc, mach_calc(i)*10000)),...
        ];
    transfer_functions = [W_AP_theta_ol, W_AP_theta, W_AP_alt, W_AP_alt_ol];
    run('bode_plots_analyze.m');

end

function [K_value] = get_K_value(K_array, q_array,  mach, height)
    [~, a, ~, rho] = atmosisa(height);
    V_target = mach.*a;
    q_target = (rho.*V_target.^2)./2;
    [~, ind] = unique(K_array);
    K_value = interp1(q_array(ind), K_array(ind), q_target,'linear');
end


function [W_AP_theta, W_AP_altitude, W_zam_1, W_raz_3] = get_control_system(mach, height, K_omega_z, K_theta, aero_data, plane, W_p)
    [~, a, ~, rho] = atmosisa(height);
    V_target = mach.*a;
    p = tf('p');
    [m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(mach, height, aero_data, plane);

    omega_0 = sqrt(-bar_M_z_alpha - bar_M_z_omega_z.*bar_Y_alpha);
    xi_k = (bar_Y_alpha - bar_M_z_omega_z - bar_M_z_dot_alpha)./(2.*omega_0);

    d_omega_d_delta_v = (bar_M_z_delta_v*(p + bar_Y_alpha))/(p^2 + 2*xi_k*omega_0*p + omega_0^2); 
    W_raz_1 = W_p*d_omega_d_delta_v;
    W_zam_1 = feedback(W_raz_1, -K_omega_z);
    W_raz_2 = -K_theta*W_zam_1*(1/p);
    W_AP_theta = feedback(W_raz_2, 1);

    T_1c = 1/bar_Y_alpha;
    K_H = V_target;
    i_H = 0.8*(1/(T_1c*V_target));

    has_overshoot = true;
    while has_overshoot
        W_H_theta = (K_H)/(p*(1 + T_1c*p));
        W_raz_3 = i_H*W_AP_theta*W_H_theta;
        W_AP_altitude = feedback(W_raz_3, 1);
        W_AP_H_step_info = stepinfo(W_AP_altitude);
        if W_AP_H_step_info.Overshoot == 0
            has_overshoot = false;
        else 
            K_H = K_H - 1;
        end
    end
    disp(['MACH CALC = ' num2str(mach)])
    disp(['overshoot= ', num2str(W_AP_H_step_info.Overshoot), ', K_H= ' ,num2str(K_H)]);
    disp(['K_H_method/K_H_my= ', num2str(V_target/K_H), '\n']);
end

function latex_string = tf_to_latex(tf_, decimal)
    syms p;
    [num, den] = tfdata(tf_, 'v');
    num = round(num, decimal);
    den = round(den, decimal);

    sys_syms = poly2sym(num, p)/poly2sym(den, p);
    latex_string = latex(vpa(sys_syms));
end


function new_matrix = increase_column_elements(matrix, number_of_elements) 
    [r, c] = size(matrix);
    new_matrix = zeros(r, number_of_elements);
    for i = 1:r
        matrix_row = matrix(i, :);
        first_value = matrix_row(1);
        last_value = matrix_row(end);
        step_size = (last_value - first_value)/number_of_elements;
        new_row = zeros(1, number_of_elements);
        new_row(1) = first_value;
        new_row(end) = last_value;
        for n_i  = 2:number_of_elements-1
            new_row(n_i) = first_value+step_size*(n_i-1);
        end
        new_matrix(i, :) = new_row;
    end
end

function closes_value = find_closest_value_in_array(array, value)
    dist = abs(array - value);
    minDist = min(min(dist));
    minIdx = (dist == minDist);
    closes_value = array(minIdx);
end

function [k, q_range] = get_trend_approx_values(K_matrix, q_matrix, points_amount)
    q_range = zeros(1,points_amount); 
    q_range(1) = min(min(q_matrix));
    q_range(end) = max(max(q_matrix));
    q_step = (q_range(end) - q_range(1))/points_amount;
    for i = 2:length(q_range)-1
        idel_step = q_range(i-1)+q_step;
        q_range(i) = find_closest_value_in_array(q_matrix, idel_step);
    end
    k = return_element_in_another_matrix(q_matrix, q_range, K_matrix);

end

function [values] = return_element_in_another_matrix(matrix1, matrix1_elements, matrix2)
    if any(size(matrix2) == 1)
        try
            for i = 1:length(matrix1_elements)
                [r, c] = find(matrix1 == matrix1_elements(i));
                values(i) = matrix2(r);
            end
        catch
            for i = 1:length(matrix1_elements)
                [r, c] = find(matrix1 == matrix1_elements(i));
                values(i) = matrix2(c);
            end
        end
    else
        if isequal(size(matrix2), size(matrix1))
            for i = 1:length(matrix1_elements)
                [r c] = find(matrix1 == matrix1_elements(i));
                values(i) = max(max(matrix2(r, c)));
            end
        elseif any(size(matrix1) == 1)
            for i = 1:length(matrix1_elements)
                n = find(matrix1 == matrix1_elements(i));
                values(i, :) = matrix2(n, :);
            end
        end

    end
end


