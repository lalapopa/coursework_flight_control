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
                    row_to_append.append(f'{el} {add_text}')
                    column_pos = np.delete(column_pos, 0)
                else:
                    row_to_append.append(el)
            new_list.append(row_to_append)
        else:
            new_list.append(row)
    return new_list 

xi_s = pd.read_csv(config.PATH_DATA_FOLDER+config.FILE_XI_S, header=None)
xi_s_max = max(xi_s.iloc[:, -1].to_numpy())

xi_s = xi_s.iloc[: , :-1]
xi_s_max_position = find_row_and_column_by_value(xi_s, xi_s_max) 
xi_s_array = xi_s.to_numpy()

text_to_add = "\\cellcolor{green}"
new_table = add_text_to_array_cell(xi_s_array, text_to_add, xi_s_max_position[0], xi_s_max_position[1])

H = pd.read_csv(config.PATH_DATA_FOLDER+config.FILE_H, header=None)
output_df = pd.DataFrame(new_table)
output_df = pd.concat([H, output_df], axis=1)
print(output_df.to_latex(escape=False, index=False))

