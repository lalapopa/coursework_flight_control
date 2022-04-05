import pandas as pd 

def convert_to_string_with_decimal_number(array, decimal_number):
    converted = []
    format_string = f'%.{decimal_number}f'
    for val in array:
        converted.append(str(format_string % (val)))
    return converted 

C_y_a = [5.5360, 5.5360, 5.5360, 5.5740, 5.7400, 6.2000]
otn_x_f = [0.6950, 0.6900, 0.6950, 0.7100, 0.7280, 0.7640]
m_z_otn_omega_z = [-10.5970, -10.5940, -10.5920, -10.5970, -10.6000, -11.6280]
m_z_bar_aa = [-2.2300, -2.2280, -2.1640, -1.8300, -1.5980, -1.5810]
m_z_phi = [-0.6048, -0.6048, -0.6048, -0.5846, -0.5578, -0.5376]
m_y_dn = [-0.2082, -0.2084, -0.2083, -0.2081, -0.2075, -0.2070]
m_y_beta = [-0.2109, -0.2130, -0.2170, -0.2200, -0.2250, -0.2320]
m_x_beta = [-0.2600, -0.2600, -0.2700, -0.2700, -0.2730, -0.2800]
m_x_omega_x = [-0.5250, -0.5250, -0.5200, -0.5070, -0.4880, -0.4750]
m_y_omega_y = [-0.3250, -0.3260, -0.3420, -0.3460, -0.3750, -0.3800]
C_z_beta = [-2.2500, -2.2900, -2.2500, -2.2080, -2.3100, -2.4000]
C_z_dn = [-0.4100, -0.4100, -0.4100, -0.4100, -0.4100, -0.4100]
m_x_dn = [-0.0300, -0.0300, -0.0300, -0.0300, -0.0310, -0.0320]
m_x_de = [-0.1170, -0.1170, -0.1150, -0.1130, -0.1090, -0.1050]
m_z_dv = [-0.9500, -0.9500, -0.9250, -0.9500, -0.9750, -0.9800]
mach = [0.3000, 0.4000, 0.5000, 0.6000, 0.7000, 0.8000]
table_1 = {
        r'$M$' : convert_to_string_with_decimal_number(mach, 1),
        r'$C_y^\alpha$': convert_to_string_with_decimal_number(C_y_a, 3),
        r'$\bar{x}_{F}$': convert_to_string_with_decimal_number(otn_x_f, 3),
        r'$m_z^{\bar{\omega}_z}$': convert_to_string_with_decimal_number(m_z_otn_omega_z, 2),
        r'$m_{z}^{\bar{\dot{\alpha}}}$': convert_to_string_with_decimal_number(m_z_bar_aa, 2),
        r'$m_{z}^{\varphi}$': convert_to_string_with_decimal_number(m_z_phi, 4),
#        r'$m_y^{\delta_{н}}$': convert_to_string_with_decimal_number(m_y_dn, 4),
#        r'$m_y^\beta$': convert_to_string_with_decimal_number(m_y_beta, 4),
#        r'$m_x^\beta$': convert_to_string_with_decimal_number(m_x_beta, 4),
        r'$m_z^{\delta_в}$': convert_to_string_with_decimal_number(m_z_dv, 4),
        }
table_2 = {
        r'$M$' : convert_to_string_with_decimal_number(mach, 1),
#        r'$m_x^{\bar{\omega}_x}$': convert_to_string_with_decimal_number(m_x_omega_x, 3),
#        r'$m_y^{\bar{\omega}_y}$': convert_to_string_with_decimal_number(m_y_omega_y, 3),
#        r'$C_z^\beta$': convert_to_string_with_decimal_number(C_z_beta, 3),
#        r'$C_z^{\delta_н}$': convert_to_string_with_decimal_number(C_z_dn, 4),
#        r'$m_x^{\delta_н}$': convert_to_string_with_decimal_number(m_x_dn, 4),
#        r'$m_x^{\delta_э}$': convert_to_string_with_decimal_number(m_x_de, 4),
        r'$m_z^{\delta_в}$': convert_to_string_with_decimal_number(m_z_dv, 4),
        }
print(pd.DataFrame(table_1).to_latex(escape=False, index=False))




