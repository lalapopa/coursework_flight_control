function [epsilon, nu] = epsilon_nu_find(mach, alt, omega_0_max, aero_data, plane, W_p, T_n)
    p = tf('p');
    [m_z_a,m_z_cy,bar_M_z_alpha,bar_M_z_dot_alpha,bar_M_z_delta_v,bar_M_z_omega_z,bar_M_z_bar_omega_z,bar_Y_alpha] = moments_values(mach, alt, aero_data, plane);

    [~, a, ~, rho] = atmosisa(alt);
    V = mach*a;
    q = (rho*V^2)/2;

    epsilon = 0.25;
    nu = omega_0_max;
    T_1c = 1/bar_Y_alpha;

    K_omega_z_gr = -(1/(bar_M_z_delta_v*T_n));
    K_omega_z = epsilon*K_omega_z_gr;
    K_theta = nu*K_omega_z;
    K_H = V;

    i_H = 0.8*(1/(T_1c*V));

    omega_0 = sqrt(-bar_M_z_alpha - bar_M_z_omega_z*bar_Y_alpha);
    xi_k = (bar_Y_alpha - bar_M_z_omega_z - bar_M_z_dot_alpha)/(2*omega_0);

    d_omega_d_delta_v = (bar_M_z_delta_v*(p + bar_Y_alpha))/(p^2 + 2*xi_k*omega_0*p + omega_0^2); 


    answer = false;
    while(~answer)
        W_raz_1 = W_p*d_omega_d_delta_v;
        W_zam_1 = feedback(W_raz_1, -K_omega_z);
        W_raz_2 = -K_theta*W_zam_1*(1/p);
        W_zam_2 = feedback(W_raz_2, 1);

        W_H_theta = K_H/(p*(1 + T_1c*p));
        W_raz_3 = i_H*W_zam_2*W_H_theta; 
        W_zam_3 = feedback(W_raz_3, 1);

        [a_out, xi, T] = damp(W_zam_3);
        xi = xi(2);

        if(xi<=0.6)
            nu = nu-0.001;
            K_theta = nu*K_omega_z;

        end
        if(xi>=1) 
            epsilon = epsilon - 0.001;
            K_omega_z = epsilon*K_omega_z_gr;
        end

        if and(xi<1, xi>0.6) || xi<0.6
            K_omega_z = epsilon*K_omega_z_gr;
            K_theta = nu*K_omega_z;
            answer = true;
        end
    end
end
