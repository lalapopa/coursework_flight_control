function [m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(mach, height, aero_data, plane)
    [~, a, ~, rho] = atmosisa(height);
    V = mach.*a;
    q = (rho.*V.^2)./2;

    m_z_a = aero_data.get_interp_value(aero_data.C_y_a, mach).*(plane.bar_x_t - aero_data.get_interp_value(aero_data.otn_x_f, mach));
    m_z_cy = m_z_a./aero_data.get_interp_value(aero_data.C_y_a, mach);

    bar_M_z_alpha = (m_z_a.*q.*plane.S.*plane.b_a)./plane.I_z;
    bar_M_z_dot_alpha = (aero_data.get_interp_value(aero_data.m_z_bar_aa, mach).*plane.b_a.^2.*plane.S.*rho.*V)./(2*plane.I_z);
    bar_M_z_delta_v = (aero_data.get_interp_value(aero_data.m_z_dv, mach).*q.*plane.S.*plane.b_a)./plane.I_z;
    bar_M_z_omega_z = (aero_data.get_interp_value(aero_data.m_z_otn_omega_z, mach).*q.*plane.S.*plane.b_a.^2)./(plane.I_z.*V);
    bar_M_z_bar_omega_z = (aero_data.get_interp_value(aero_data.m_z_otn_omega_z, mach).*q.*plane.S.*plane.b_a)./plane.I_z;
    bar_Y_alpha = (aero_data.get_interp_value(aero_data.C_y_a, mach).*q.*plane.S)./(plane.m.*V);
end
