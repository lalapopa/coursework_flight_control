run('data.m');
run('omega_0_max_xi_s_max_find.m');
FOLDER = '~/Documents/uni/4_course/2_sem/flight_control/cource_work/code/data/'
aero_data = AeroDynamicsData;

p = tf('p');
i = 5;
mach = calc_mach(i, 2)
height = H_array(i)
[m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(mach, height, aero_data, plane);

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

epsilon = 0.25

[m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(calc_mach, H_array, aero_data, plane);

[~, a, ~, rho] = atmosisa(H_array);
V = calc_mach.*a;
q = (rho.*V.^2)/2;

omega_0 = sqrt(-bar_M_z_alpha - bar_M_z_omega_z.*bar_Y_alpha);
K_omega_z_gr = -(1./(bar_M_z_delta_v.*T_n));
K_omega_z = epsilon.*K_omega_z_gr;
K_theta = omega_0.*K_omega_z;

csvwrite([FOLDER 'K_omega_z_all.csv'], K_omega_z);
csvwrite([FOLDER 'K_theta_all.csv'], K_theta);
csvwrite([FOLDER 'q_all.csv'], q);
csvwrite([FOLDER 'H_all.csv'], H_array);


%%%%%%%%%%%%%%%%
%  A/P \theta  %
%%%%%%%%%%%%%%%%

%d_omega_d_delta_v = (bar_M_z_delta_v*(p + bar_Y_alpha))/(p^2 + 2*xi_k*omega_0*p + omega_0^2); 
%W_raz_1 = W_p*d_omega_d_delta_v;
%W_zam_1 = feedback(W_raz_1, -K_omega_z);
%W_raz_2 = -K_theta*W_zam_1*(1/p);
%W_CL = feedback(W_raz_2, 1);


%%%%%%%%%%%%
%%  A/P H  %
%%%%%%%%%%%%
%K_H = V;
%T_1c = 1/bar_Y_alpha;
%W_H_theta = (K_H)/(p*(1 + T_1c*p));
%
%A=[
%-bar_Y_alpha  1;
%(bar_M_z_alpha - bar_M_z_dot_alpha *  bar_Y_alpha)  (bar_M_z_dot_alpha + bar_M_z_omega_z);
%];
%
%B = [
%    0;
%bar_M_z_delta_v;
%    ];
%
%C = [
%1 0;
%0 1;
%];
%
%D = [ 0 ; 0];
%W = tf(ss(A,B,C,D));
%W_alpha_delta_v = W(1);
%W_omega_z_delta_v = W(2);

function closes_value = find_closest_value_in_array(array, value)
    dist = abs(array - value);
    minDist = min(dist);
    minIdx = (dist == minDist);
    closes_value = array(minIdx);
end



