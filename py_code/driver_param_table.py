import pandas as pd 
import numpy as np
import config

def find_row_and_column_by_value(data_frame, value):
    return np.where(data_frame == value)

def add_text_to_array_cell(matrix, add_text, row_pos, column_pos):
    new_list = []
    for i_r, row in enumerate(matrix): 
        if i_r in row_pos: 
            row_pos = np.delete(row_pos, 0)
            row_to_append = []
            for i_e, el in enumerate(row):
                if i_e in column_pos:
                    row_to_append.append(f'{el}{add_text}')
                    column_pos = np.delete(column_pos, 0)
                else:
                    row_to_append.append(el)
            new_list.append(row_to_append)
        else:
            new_list.append(row)
    return new_list 

omega_0 = pd.read_csv(config.PATH_DATA+config.FILE_OMEGA_0_PR, header=None)
omega_0_max = max(omega_0.iloc[:, -1].to_numpy())

omega_0 = omega_0.iloc[: , :-1]
omega_0_max_position = find_row_and_column_by_value(omega_0, omega_0_max) 
omega_0_array = omega_0.to_numpy()

text_to_add = "\\cellcolor{green}"
new_table = add_text_to_array_cell(omega_0_array, text_to_add, omega_0_max_position[0], omega_0_max_position[1])

H = pd.read_csv(config.PATH_DATA+config.FILE_H, header=None)
output_df = pd.DataFrame(new_table)
output_df = pd.concat([H, output_df], axis=1)
print(output_df.to_latex(escape=False, index=False))


