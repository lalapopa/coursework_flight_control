import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

def get_row(df, i):
    return df.iloc[i].to_numpy()

def make_simple_plot(x, y, label_text, xlabel, ylabel, file_name, limit_x=None, limit_y=None):
    plt.plot(x, y, 'o-', label=label_text, linewidth=4)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend()
    plt.grid()
    if limit_x:
        margin_5_per = (np.max(limit_x)*5)/100
        limit_x[-1] = limit_x[-1] + margin_5_per 
        plt.xlim(limit_x)
    if limit_y:
        margin_5_per = (np.max(limit_y)*5)/100
        limit_y[-1] = limit_y[-1] + margin_5_per 
        plt.ylim(limit_y)
    plt.savefig(PATH_DATA_FOLDER + file_name)
    plt.clf()

def generate_table_k_theta_k_omega(H, q, K_theta, K_omega): 
    df = pd.DataFrame()
    for i, alt in enumerate(H):
        K_theta_row = get_row(K_theta, i)
        K_omega_row = get_row(K_omega, i)
        q_row = get_row(q, i)
        first_column = [str(f'$H={alt}$, м'), '$q, \\frac{кг}{м \\,с^2}$', '$K_{\\vartheta}$', '$K_{\\omega_z}$']
        second_column = [q_row[0], K_theta_row[0], K_omega_row[0]]
        third_column = [q_row[1], K_theta_row[1], K_omega_row[1]]
        fourth_column = [q_row[2], K_theta_row[2], K_omega_row[2]]
        chunk = {
                r'$q_{min}$': second_column, 
                r'$q_{кр}$': third_column, 
                r'$q_{max}$': fourth_column,
                }
        df2 = pd.DataFrame(chunk)
        df2.index = pd.MultiIndex.from_tuples([
            (str('$H=%s$, м' % (alt)), r'$q, \frac{кг}{м \,с^2}$'), 
            (str('$H=%s$, м' % (alt)), r'$K_{\vartheta}$'), 
            (str('$H=%s$, м' % (alt)), r'$K_{\omega_z}$')
            ])
        df = pd.concat([df, df2])

    print(df.to_latex(escape=False))



PATH_DATA_FOLDER = '/home/lalapopa/Documents/uni/4_course/2_sem/flight_control/cource_work/code/data/'
FILE_NAME_H = 'H_all.csv'
FILE_NAME_K_OMEGA_Z = 'K_omega_z_all.csv'
FILE_NAME_K_THETA = 'K_theta_all.csv'
FILE_NAME_Q = 'q_all.csv'

altitudes = pd.read_csv(PATH_DATA_FOLDER + FILE_NAME_H, header=None) 
q = pd.read_csv(PATH_DATA_FOLDER + FILE_NAME_Q, header=None) 
K_omega_z = pd.read_csv(PATH_DATA_FOLDER + FILE_NAME_K_OMEGA_Z, header=None) 
K_theta = pd.read_csv(PATH_DATA_FOLDER + FILE_NAME_K_THETA, header=None) 

q_global_max = np.max(q.max().to_numpy())
K_omega_z_global_max = np.max(K_omega_z.max().to_numpy())
K_theta_global_max = np.max(K_omega_z.max().to_numpy())

H_array = []
for i in range(0, len(altitudes)):
    H = get_row(altitudes, i)[0]
    H_array.append(H)
    K_omega_z_row = get_row(K_omega_z, i)
    K_theta_row = get_row(K_theta, i)
    q_row= get_row(q, i)
#    make_simple_plot(q_row, K_omega_z_row, 
#            '$K_{\\omega_z}(q), H=%s$ м' % (H),
#            '$q, [\\frac{кг}{м \\,с^2}$]', '$K_{\\omega_z}$', 'k_omega_z_%s.png' % (H),
#            [0, q_global_max],
#            [0, K_omega_z_global_max],
#            )
#    make_simple_plot(q_row, K_theta_row, 
#            '$K_{\\vartheta}(q), H=%s$ м' % (H),
#            '$q, [\\frac{кг}{м \\,с^2}$]', '$K_{\\vartheta}$', 'k_theta_%s.png' % (H),
#            [0, q_global_max],
#            [0, K_theta_global_max],
#            )

H_target = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, H_array[-1]]
H_indices = [i for i, val in enumerate(H_array) if val in H_target]
generate_table_k_theta_k_omega(H_target, q.iloc[H_indices], K_theta.iloc[H_indices], K_omega_z.iloc[H_indices])


    


