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

[r, c] = size(calc_mach);
K_omega_z = zeros(r, c);
K_theta = zeros(r, c);
K_H = zeros(r, c);
i_H = zeros(r, c);
V = zeros(r, c);
q = zeros(r, c);

for i = 1:r 
    for j = 1:c
        [epsilon, nu] = epsilon_nu_find(calc_mach(i, j), H_array(i), omega_0_max, aero_data, plane, W_p, T_n);
        [~,~,~,~,bar_M_z_delta_v,~,~,bar_Y_alpha] = moments_values(calc_mach(i,j), H_array(r), aero_data, plane);
        disp(['epsilon=', num2str(epsilon), 'nu=', num2str(nu)]);
        [~, a, ~, rho] = atmosisa(H_array(i));
        
        V(i, j) = calc_mach(i, j).*a;
        q(i, j) = (rho.*V(i,j).^2)/2;
        T_1c = 1/bar_Y_alpha;

        K_omega_z_gr = 1./(abs(bar_M_z_delta_v).*T_n);
        K_omega_z(i, j) = epsilon.*K_omega_z_gr;
        K_theta(i, j) = nu.*K_omega_z(i, j);
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
csvwrite([FOLDER 'fine_K_omega_z.csv'], K_omega_z_calc);
csvwrite([FOLDER 'fine_K_theta.csv'], K_theta_calc);
csvwrite([FOLDER 'fine_q.csv'], q_calc);


%%%%%%%%%%%%%%%%%
%%  A/P \theta  %
%%%%%%%%%%%%%%%%%

H_calc = 10000; % Level flight
[~, a, ~, rho] = atmosisa(H_calc);

mach_calc = return_element_in_another_matrix(H_array, H_calc, calc_mach);
V_target = mach_calc.*a;
q_target = (rho.*V_target.^2)./2;

[~, ind] = unique(K_omega_z_calc)
K_omega_z_int = interp1(q_calc(ind), K_omega_z_calc(ind), q_target,'linear');

[~, ind] = unique(K_theta_calc)
K_theta_int = interp1(q_calc(ind), K_theta_calc(ind), q_target,'linear');

[m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(mach_calc, H_calc, aero_data, plane);

omega_0 = sqrt(-bar_M_z_alpha - bar_M_z_omega_z.*bar_Y_alpha);
xi_k = (bar_Y_alpha - bar_M_z_omega_z - bar_M_z_dot_alpha)./(2.*omega_0);

i = 1;

disp(['MACH CALC = ' num2str(mach_calc(i))])
d_omega_d_delta_v = (bar_M_z_delta_v(i)*(p + bar_Y_alpha(i)))/(p^2 + 2*xi_k(i)*omega_0(i)*p + omega_0(i)^2); 
W_raz_1 = W_p*d_omega_d_delta_v;
W_zam_1 = feedback(W_raz_1, -K_omega_z_int(i));
W_raz_2 = -K_theta_int(i)*W_zam_1*(1/p);
W_AP_theta = feedback(W_raz_2, 1);

%%%%%%%%%%%
%  A/P H  %
%%%%%%%%%%%

T_1c = 1/bar_Y_alpha(i);

K_H = V_target(i);
i_H = 0.8*(1/(T_1c*V_target(i)));

W_H_theta = (K_H)/(p*(1 + T_1c*p));
W_raz_3 = i_H*W_AP_theta*W_H_theta;
W_AP_H = feedback(W_raz_3, 1);


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
                values(i) = matrix2(r, c);
            end
        elseif any(size(matrix1) == 1)
            for i = 1:length(matrix1_elements)
                n = find(matrix1 == matrix1_elements(i));
                values(i, :) = matrix2(n, :);
            end
        end

    end
end


