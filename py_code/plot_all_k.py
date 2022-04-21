import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import sys
import config
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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

input_argv = sys.argv[1:]

if not input_argv:
    print(
    'Add following possition arguments:\n\
    \n\
    -s, save all plots in /figures folder for report\n\
    -t, print LaTeX table\
            ')

def get_row(df, i):
    return df.iloc[i].to_numpy()

def find_row_and_column_by_value(data_frame, value):
    return np.where(data_frame == value)

def make_simple_plot(x, y, label_text, xlabel, ylabel, limit_x=None, limit_y=None, marker='o-'):
    plt.plot(x, y, marker, label=label_text, linewidth=4, markersize=10)
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

def generate_table_k_theta_k_omega(H, q, K_theta, K_omega, K_H, i_H): 
    df = pd.DataFrame()
    for i, alt in enumerate(H):
        K_theta_row = get_row(K_theta, i)
        K_omega_row = get_row(K_omega, i)
        K_H_row = get_row(K_H, i)
        q_row = get_row(q, i)
        i_H_row = get_row(i_H, i)

        value_column_q = [
                str(r'$q_{min}= %s \frac{кг}{м \,с^2}$' % (str(int(q_row[0])))),
                str(r'$q_{кр}= %s \frac{кг}{м \,с^2}$' % (str(int(q_row[1])))),
                str(r'$q_{max}= %s \frac{кг}{м \,с^2}$' % (str(int(q_row[2])))),
                    ] 
        value_column_1 = [str('%.2f' % (val)) for val in K_theta_row ]
        value_column_2 = [str('%.2f' % (val)) for val in K_omega_row]
        value_column_3 = [str('%.2f' % (val)) for val in K_H_row]
        value_column_4 = [str('%.6f' % (val)) for val in i_H_row]

        chunk = {
                r'$K_{\vartheta}$': value_column_1,
                r'$K_{\omega_z}$': value_column_2,
                r'$K_{H}$': value_column_3,
                r'$i_H$': value_column_4,
                }

        df2 = pd.DataFrame(chunk)
        df2.index = pd.MultiIndex.from_tuples([
            (str('$H=%s$, м' % (alt)),value_column_q[0]), 
            (str('$H=%s$, м' % (alt)),value_column_q[1]), 
            (str('$H=%s$, м' % (alt)),value_column_q[2]),
            ])
        df = pd.concat([df, df2])
    latex_table = df.to_latex(escape=False)
    return format_latex_table(latex_table)

def format_latex_table(latex_string):
    re_hline = r'\\hline'
    number_of_column = len(list(re.findall(r"(?<={)l*(?=})", latex_string)[0]))
    new_prefix = '|'+'c|'*number_of_column
    latex_string = re.sub(r'(?<={)l*(?=})', new_prefix, latex_string)
    latex_string = re.sub(r'(\\bottomrule)|(\\midrule)|(\\toprule)', re_hline, latex_string)
    
    main_table = latex_string.splitlines()[4:]
    match_H = r'(?<=\$)H=[\d]*(?=\$)'

    counter = 0
    formated_latex_table = '\n'.join([str(j) for j in latex_string.splitlines()[0:4]])
    for i, line in enumerate(main_table):
        if re.search(match_H, line) or i == len(main_table)-3 or i == len(main_table)-1:
            counter = 0
        else:
            counter += 1
        if counter == 2:
            new_line = '\n'+line+'\hline' 
        else:
            new_line = '\n'+line
        formated_latex_table += f"{new_line}" 
    return formated_latex_table

def save_string_to_file(input_data, file_name):
    with open(file_name, "w") as f:
        f.write(input_data)

def get_values_by_row_column(df, row_column_index_arrays):
    rows = row_column_index_arrays[0]
    columns = row_column_index_arrays[-1]
    value = []
    for i, val in enumerate(rows): 
        value.append(df.iat[val, columns[i]])
    return value

def plot_from_arrays(alts, x_values, y_values, legend_name, x_label, y_label): 
    markers = [ "v", "^", "<", ">", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D"]

    for i in range(0, len(alts)):
        H = get_row(alts, i)[0]
        y_row = get_row(y_values, i)
        x_row = get_row(x_values, i)
        make_simple_plot(x_row, y_row, 
                legend_name % (H),
                x_label, y_label,
                marker=markers[i]+'-'
                )

def save_figure(save_path):
    if '-s' in input_argv:
        plt.legend()
        plt.grid()
        plt.savefig(save_path)
        print(f'figure saved in {save_path}')
        plt.clf()



altitudes = pd.read_csv(config.PATH_DATA + config.FILE_H, header=None) 
q = pd.read_csv(config.PATH_DATA + config.FILE_Q, header=None) 
K_omega_z = pd.read_csv(config.PATH_DATA + config.FILE_K_OMEGA_Z, header=None) 
K_theta = pd.read_csv(config.PATH_DATA + config.FILE_K_THETA, header=None) 
K_H = pd.read_csv(config.PATH_DATA + config.FILE_K_H, header=None) 
i_H = pd.read_csv(config.PATH_DATA + config.FILE_i_H, header=None) 

q_global_max = np.max(q.max().to_numpy())
K_omega_z_global_max = np.max(K_omega_z.max().to_numpy())
K_theta_global_max = np.max(K_omega_z.max().to_numpy())


plot_from_arrays(altitudes, q, K_omega_z, 
        '$K_{\\omega_z}(q), H=%s$ м',
        '$q, [\\frac{кг}{м \\,с^2}$]', '$K_{\\omega_z}$'
        )
fine_q = np.genfromtxt(config.PATH_DATA + 'fine_q.csv', delimiter=',')
fine_K_omega_z = np.genfromtxt(config.PATH_DATA + 'fine_K_omega_z.csv', delimiter=',')
plt.plot(fine_q, fine_K_omega_z, 'ko--', label='$K_{\\omega_z}$ выбранное')

save_figure(config.PATH_SAVE+'K_omega_z_H_q.pgf')


plot_from_arrays(altitudes, q, K_theta, 
        '$K_{\\vartheta}(q), H=%s$ м',
        '$q, [\\frac{кг}{м \\,с^2}$]', '$K_{\\vartheta}$', 
        )
fine_K_theta = np.genfromtxt(config.PATH_DATA + 'fine_K_theta.csv', delimiter=',')
plt.plot(fine_q, fine_K_theta, 'ko--', label='$K_{\\vartheta}$ выбранное')

save_figure(config.PATH_SAVE + 'K_theta_H_q.pgf')

plot_from_arrays(altitudes, q, K_H, 
        '$K_{H}(q), H=%s$ м',
        '$q, [\\frac{кг}{м \\,с^2}$]', '$K_{H}$', 
        )

save_figure(config.PATH_SAVE + 'K_H_H_q.pgf')


plot_from_arrays(altitudes, q, i_H, 
        '$i_{H}(q), H=%s$ м',
        '$q, [\\frac{кг}{м \\,с^2}$]', '$i_{H}$', 
        )
save_figure(config.PATH_SAVE + 'i_H_H_q.pgf')


if '-t' in input_argv:
    H_target = np.hstack(altitudes.to_numpy())
    H_indices = [i for i, val in enumerate(H_target) if val in H_target]
    latex_table = generate_table_k_theta_k_omega(H_target, q.iloc[H_indices], K_theta.iloc[H_indices], K_omega_z.iloc[H_indices], K_H.iloc[H_indices], i_H.iloc[H_indices])

    file_name = config.PATH_REPORT+'table_coeffs.tex'
    save_string_to_file(latex_table, file_name)
    print(f'Saved table in {file_name}')

