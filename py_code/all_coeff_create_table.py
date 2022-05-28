import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import config
import re
import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.simplefilter("ignore", FutureWarning)

def get_row(df, i):
    return df.iloc[i].to_numpy()

def generate_table_k_theta_k_omega(H, mach, K_theta, K_omega, K_H, i_H): 
    df = pd.DataFrame()
    H_array = np.unique(H.to_numpy())
    for i, alt in enumerate(H_array):
        K_theta_row = get_row(K_theta, i)
        K_omega_row = get_row(K_omega, i)
        K_H_row = get_row(K_H, i)
        mach_row = get_row(mach, i)
        i_H_row = get_row(i_H, i)

        value_column_text = [
                str(r'$M$'),
                str(r'$K_\vartheta$'),
                str(r'$K_{\omega_z}$'),
                str(r'$K_H$'),
                str(r'$i_H$'),
                    ] 

        value_column_1 = [str('%.2f' % (val)) for val in K_theta_row ]
        value_column_2 = [str('%.2f' % (val)) for val in K_omega_row]
        value_column_3 = [str('%.0f' % (val)) for val in K_H_row]
        value_column_4 = [str('%.6f' % (val)) for val in i_H_row]
        value_column_5 = [str('%.3f' % (val)) for val in mach_row]

        rows = np.array([
            value_column_5,
            value_column_1,
            value_column_2,
            value_column_3,
            value_column_4,
            ])

#        chunk = {
#                r'$M$': value_column_5,
#                r'$K_{\vartheta}$': value_column_1,
#                r'$K_{\omega_z}$': value_column_2,
#                r'$K_{H}$': value_column_3,
#                r'$i_H$': value_column_4,
#                }

        
        index = pd.MultiIndex.from_product([[f'{alt}'], 
            value_column_text], 
            names=['$H$', ' '])
        df2 = pd.DataFrame(index=index, data=rows)
        df = pd.concat([df, df2])

    latex_table = df.to_latex(escape=False)
    return format_latex_table(latex_table)

def format_latex_table(latex_string):
    re_hline = r'\\hline'
    number_of_column = len(list(re.findall(r"(?<={)l*(?=})", latex_string)[0]))
    new_prefix = '|'+'c|'*number_of_column
    latex_string = re.sub(r'(?<={)l*(?=})', new_prefix, latex_string)
    latex_string = re.sub(r'(\\bottomrule)|(\\midrule)|(\\toprule)', re_hline, latex_string)
    
    main_table = latex_string.splitlines()[5:]

    formated_latex_table = '' 
    for i, line in enumerate(latex_string.splitlines()[0:5]):
        if i == 2:
            continue 
        if i == 3:
            formated_latex_table += r'$H,\ м$ & \multicolumn{%s}{c|}{}\\' % (number_of_column-1)
            continue
        formated_latex_table += f"{line}\n"

    counter = 0
    match_H = r'^\d+'
    for i, line in enumerate(main_table):
        if re.search(match_H, line) or i == len(main_table)-3:
            counter = 0
        else:
            counter += 1
        if counter == 4:
            new_line = '\n'+line+'\hline' 
        else:
            new_line = '\n'+line
        formated_latex_table += f"{new_line}" 
    return formated_latex_table

def save_string_to_file(input_data, file_name):
    with open(file_name, "w") as f:
        f.write(input_data)

altitudes = pd.read_csv(config.PATH_DATA + config.FILE_H, header=None) 
mach = pd.read_csv(config.PATH_DATA + config.FILE_MACH_AREA, header=None) 
K_omega_z = pd.read_csv(config.PATH_DATA + config.FILE_K_OMEGA_Z, header=None) 
K_theta = pd.read_csv(config.PATH_DATA + config.FILE_K_THETA, header=None) 
K_H = pd.read_csv(config.PATH_DATA + config.FILE_K_H, header=None) 
i_H = pd.read_csv(config.PATH_DATA + config.FILE_i_H, header=None) 

latex_table = generate_table_k_theta_k_omega(altitudes, mach, K_theta, K_omega_z, K_H, i_H)
file_name = config.PATH_REPORT+'table_coeffs.tex'
save_string_to_file(latex_table, file_name)
print(f'Saved table in {file_name}')
