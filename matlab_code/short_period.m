clear all;
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

run('epsilon_nu_find.m');

[m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(calc_mach, H_array, aero_data, plane);

[~, a, ~, rho] = atmosisa(H_array);
V = calc_mach.*a;
q = (rho.*V.^2)/2;

omega_0 = sqrt(-bar_M_z_alpha - bar_M_z_omega_z.*bar_Y_alpha);
K_omega_z_gr = -(1./(bar_M_z_delta_v.*T_n));
K_omega_z = epsilon.*K_omega_z_gr;
K_theta = nu.*K_omega_z;

K_omega_z_calc = max(K_omega_z);
K_theta_calc = max(K_theta);
V_calc = return_element_in_another_matrix(K_omega_z, K_omega_z_calc, V);
mach_calc = return_element_in_another_matrix(K_omega_z, K_omega_z_calc, calc_mach);
H_calc = return_element_in_another_matrix(K_omega_z, K_omega_z_calc, H_array);

csvwrite([FOLDER 'K_omega_z_all.csv'], K_omega_z);
csvwrite([FOLDER 'K_theta_all.csv'], K_theta);
csvwrite([FOLDER 'q_all.csv'], q);
csvwrite([FOLDER 'H_all.csv'], H_array);
csvwrite([FOLDER 'omega_0_pr.csv'], omega_0_H_M);
csvwrite([FOLDER 'fine_K_omega_z.csv'], K_omega_z_calc);
csvwrite([FOLDER 'fine_K_theta.csv'], K_theta_calc);

%%%%%%%%%%%%%%%%%
%%  A/P \theta  %
%%%%%%%%%%%%%%%%%

[m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(mach_calc, H_calc, aero_data, plane);

omega_0 = sqrt(-bar_M_z_alpha - bar_M_z_omega_z.*bar_Y_alpha);
xi_k = (bar_Y_alpha - bar_M_z_omega_z - bar_M_z_dot_alpha)./(2.*omega_0);

i = 1 
d_omega_d_delta_v = (bar_M_z_delta_v(i)*(p + bar_Y_alpha(i)))/(p^2 + 2*xi_k(i)*omega_0(i)*p + omega_0(i)^2); 
W_raz_1 = W_p*d_omega_d_delta_v;
W_zam_1 = feedback(W_raz_1, -K_omega_z(i));
W_raz_2 = -K_theta(i)*W_zam_1*(1/p);
W_AP_theta = feedback(W_raz_2, 1);

%%%%%%%%%%%%
%%  A/P H  %
%%%%%%%%%%%%
T_1c = 1/bar_Y_alpha(i);

K_H = V_calc(i)
i_H = 0.8*(1/(T_1c*V_calc(i)))

W_H_theta = (K_H)/(p*(1 + T_1c*p));
W_raz_3 = i_H*W_AP_theta*W_H_theta;






function closes_value = find_closest_value_in_array(array, value)
    dist = abs(array - value);
    minDist = min(dist);
    minIdx = (dist == minDist);
    closes_value = array(minIdx);
end

function [values] = return_element_in_another_matrix(matrix1, matrix1_elements, matrix2)
    if any(size(matrix2) == 1)
        for i = 1:length(matrix1_elements)
            [r c] = find(matrix1 == matrix1_elements(i));
            values(i) = matrix2(r);
        end
    else
        for i = 1:length(matrix1_elements)
            [r c] = find(matrix1 == matrix1_elements(i));
            values(i) = matrix2(r, c);
        end
    end
end


