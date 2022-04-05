aero_data = AeroDynamicsData;

for height = H_array 
    [~, a, ~, rho] = atmosisa(height);
    V = calc_mach.*a;
    q = (rho.*V.^2)./2;
        
    m_z_a = aero_data.get_interp_value(aero_data.C_y_a, calc_mach).*(plane.bar_x_t - aero_data.get_interp_value(aero_data.otn_x_f, calc_mach));

    bar_M_z_alpha = (m_z_a.*q.*plane.S.*plane.b_a)./plane.I_z;
    bar_M_z_dot_alpha = (aero_data.get_interp_value(aero_data.m_z_bar_aa, calc_mach).*plane.b_a^2.*plane.S.*rho.*V)./(2.*plane.I_z);
    bar_M_z_omega_z = (aero_data.get_interp_value(aero_data.m_z_otn_omega_z, calc_mach).*q.*plane.S.*plane.b_a^2)./(plane.I_z.*V);
    bar_Y_alpha = (aero_data.get_interp_value(aero_data.C_y_a, calc_mach).*q.*plane.S)./(plane.m.*V);
    omega_0_H_M = sqrt(- bar_M_z_alpha - bar_M_z_omega_z.*bar_Y_alpha);
    xi_k = (bar_Y_alpha - bar_M_z_omega_z - bar_M_z_dot_alpha)./(2.*omega_0_H_M);
end


xi_s_max = max(xi_k, [], 'all');
[r, c] = find(xi_k==xi_s_max);
H_calc_xi = H_array(r); 
mach_calc_xi = V(r,c)/a(r);  

omega_0_max = max(omega_0_H_M, [], 'all');
[r, c] = size(omega_0_H_M);
omega_0_H_M(1, c+1) = omega_0_max;

to_delete = {'aero_data','height','V', 'q', 'bar_M_z_alpha', 'bar_M_z_omega_z', 'bar_Y_alpha', 'xi_k'};
clear(to_delete{:});
