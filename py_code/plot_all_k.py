import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams.update(matplotlib.rcParamsDefault)
matplotlib.use("pgf")
matplotlib.rcParams.update(
{
"pgf.texsystem": "pdflatex",
"font.family": "serif",
"text.usetex": True,
"pgf.rcfonts": False,
"pgf.preamble": "\n".join(
[
r"\usepackage[warn]{mathtext}",
r"\usepackage[T2A]{fontenc}",
r"\usepackage[utf8]{inputenc}",
r"\usepackage[english,russian]{babel}",
]
),
}
)
def get_row(df, i):
    return df.iloc[i].to_numpy()

def find_row_and_column_by_value(data_frame, value):
    return np.where(data_frame == value)

def make_simple_plot(x, y, label_text, xlabel, ylabel, limit_x=None, limit_y=None):
    plt.plot(x, y, 'o-', label=label_text, linewidth=4)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    if limit_x:
        margin_5_per = (np.max(limit_x)*5)/100
        limit_x[-1] = limit_x[-1] + margin_5_per 
        plt.xlim(limit_x)
    if limit_y:
        margin_5_per = (np.max(limit_y)*5)/100
        limit_y[-1] = limit_y[-1] + margin_5_per 
        plt.ylim(limit_y)

def generate_table_k_theta_k_omega(H, q, K_theta, K_omega): 
    df = pd.DataFrame()
    for i, alt in enumerate(H):
        K_theta_row = get_row(K_theta, i)
        K_omega_row = get_row(K_omega, i)
        q_row = get_row(q, i)
        first_column = [str(f'$H={alt}$, м'), '$q, \\frac{кг}{м \\,с^2}$', '$K_{\\vartheta}$', '$K_{\\omega_z}$']
        second_column = [int(q_row[0]), str('%.2f' % (K_theta_row[0])), str('%.2f' % (K_omega_row[0]))]
        third_column = [int(q_row[1]), str('%.2f' % (K_theta_row[1])), str('%.2f' % (K_omega_row[1]))]
        fourth_column = [int(q_row[2]), str('%.2f' % (K_theta_row[2])), str('%.2f' % (K_omega_row[2]))]
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

def get_values_by_row_column(df, row_column_index_arrays):
    rows = row_column_index_arrays[0]
    columns = row_column_index_arrays[-1]
    value = []
    for i, val in enumerate(rows): 
        value.append(df.iat[val, columns[i]])
    return value


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

pos_K_omega_z = find_row_and_column_by_value(K_omega_z, K_omega_z.max())
q_K_omega_z = get_values_by_row_column(q, pos_K_omega_z)

H_array = []
for i in range(0, len(altitudes)):
    H = get_row(altitudes, i)[0]
    H_array.append(H)
    K_omega_z_row = get_row(K_omega_z, i)
    q_row= get_row(q, i)
    make_simple_plot(q_row, K_omega_z_row, 
            '$K_{\\omega_z}(q), H=%s$ м' % (H),
            '$q, [\\frac{кг}{м \\,с^2}$]', '$K_{\\omega_z}$',
            )

fine_K_omega_z = np.genfromtxt(PATH_DATA_FOLDER + 'fine_K_omega_z.csv', delimiter=',')
plt.plot(q_K_omega_z, fine_K_omega_z, 'ko--', label='$K_{\\omega_z}$ выбранное')
plt.legend()
plt.grid()
plt.savefig(PATH_DATA_FOLDER + 'K_omega_z_H_q.pgf')
plt.clf()

pos_K_theta = find_row_and_column_by_value(K_theta, K_theta.max())
q_K_theta = get_values_by_row_column(q, pos_K_theta)

H_array = []
for i in range(0, len(altitudes)):
    H = get_row(altitudes, i)[0]
    H_array.append(H)
    K_theta_row = get_row(K_theta, i)
    q_row= get_row(q, i)
    make_simple_plot(q_row, K_theta_row, 
            '$K_{\\vartheta}(q), H=%s$ м' % (H),
            '$q, [\\frac{кг}{м \\,с^2}$]', '$K_{\\vartheta}$', 
            )
fine_K_theta = np.genfromtxt(PATH_DATA_FOLDER + 'fine_K_theta.csv', delimiter=',')
plt.plot(q_K_theta, fine_K_theta, 'ko--', label='$K_{\\vartheta}$ выбранное')
plt.legend()
plt.grid()
plt.savefig(PATH_DATA_FOLDER + 'K_theta_H_q.pgf')
plt.clf()

H_target = H_array 
H_indices = [i for i, val in enumerate(H_array) if val in H_target]
#generate_table_k_theta_k_omega(H_target, q.iloc[H_indices], K_theta.iloc[H_indices], K_omega_z.iloc[H_indices])

