[m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(mach_calc_xi, H_calc_xi, aero_data, plane);

clear a rho;
[~, a, ~, rho] = atmosisa(H_calc_xi);
V = mach_calc_xi*a;
q = (rho*V^2)/2;

epsilon = 0.25;
h = 0.25;
nu = omega_0_max;
T_1c = 1/bar_Y_alpha;

K_omega_z_gr = -(1/(bar_M_z_delta_v*T_n));
K_omega_z = epsilon*K_omega_z_gr;
K_theta = nu*K_omega_z;
K_H = h*K_theta;

i_H = 0.8*(1/(T_1c*V));

omega_0 = sqrt(-bar_M_z_alpha - bar_M_z_omega_z*bar_Y_alpha);
xi_k = (bar_Y_alpha - bar_M_z_omega_z - bar_M_z_dot_alpha)/(2*omega_0);

d_omega_d_delta_v = (bar_M_z_delta_v*(p + bar_Y_alpha))/(p^2 + 2*xi_k*omega_0*p + omega_0^2); 

%    W_H_theta = K_H/(p*(1 + T_1c*p));
%    W_raz_3 = i_H*W_zam_2; 
%    W_zam_3 = feedback(W_raz_3, W_H_theta);
answer = false;
while(~answer)
    W_raz_1 = W_p*d_omega_d_delta_v;
    W_zam_1 = feedback(W_raz_1, -K_omega_z);
    W_raz_2 = -K_theta*W_zam_1*(1/p);
    W_zam_2 = feedback(W_raz_2, 1);
    [a_out, xi, T] = damp(W_zam_2);
    xi = xi(2);

    if(xi<=0.6)
        nu = nu-0.001;
        K_theta = nu*K_omega_z;
    end
    if(xi>=1) 
%            h = h-0.001;
        epsilon = epsilon - 0.001;
        K_omega_z = epsilon*K_omega_z_gr;
%            K_H=h*K_v;
    end
    if and(xi<1, xi>0.6) | xi<0.6
%            K_H = h*K_theta;
        K_omega_z = epsilon*K_omega_z_gr;
        K_theta = nu*K_omega_z;
        answer = true;
    end
end
