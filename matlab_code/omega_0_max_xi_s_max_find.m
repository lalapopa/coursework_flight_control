aero_data = AeroDynamicsData;

for height = H_array 
    [~, a, ~, rho] = atmosisa(height);
    V = mach.*a;
    q = (rho.*V.^2)/2;
        
    m_z_a = aero_data.get_interp_value(aero_data.C_y_a, mach).*(plane.bar_x_t - aero_data.get_interp_value(aero_data.otn_x_f, mach));

    bar_M_z_alpha = (m_z_a.*q.*plane.S.*plane.b_a)./plane.I_z;
    bar_M_z_dot_alpha = (aero_data.get_interp_value(aero_data.m_z_bar_aa, mach).*plane.b_a^2.*plane.S.*rho.*V)./(2*plane.I_z);
    bar_M_z_omega_z = (aero_data.get_interp_value(aero_data.m_z_otn_omega_z, mach).*q.*plane.S*plane.b_a^2)./(plane.I_z.*V);
    bar_Y_alpha = (aero_data.get_interp_value(aero_data.C_y_a, mach).*q.*plane.S)./(plane.m.*V);
    omega_0 = sqrt(- bar_M_z_alpha - bar_M_z_omega_z.*bar_Y_alpha);
    xi_k = (bar_Y_alpha - bar_M_z_omega_z - bar_M_z_dot_alpha)./(2.*omega_0);
end


xi_s_max = max(xi_k, [], 'all');
[r, c] = find(xi_k==xi_s_max);
H_calc_xi = H_array(r); 
mach_calc_xi = V(r,c)/a(r);  

omega_0_max = max(omega_0, [], 'all');
to_delete = {'aero_data','height','V', 'q', 'omega_0', 'bar_M_z_alpha', 'bar_M_z_omega_z', 'bar_Y_alpha', 'xi_k'};
clear(to_delete{:});
