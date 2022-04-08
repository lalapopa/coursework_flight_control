import pandas as pd

def convert_to_string_with_decimal_number(array, decimal_number):
    converted = []
    format_string = f'%.{decimal_number}f'
    for val in array:
        converted.append(str(format_string % (val)))
    return converted 

file_name = 'table_2.csv'

df = pd.read_csv(file_name).rename(columns={'Unnamed: 0': 'H'})
H = df['H'].to_numpy()*1000
M_min = df['M_min'].to_numpy()
M_max = df['M_max'].to_numpy()
M_4 = df['M_4'].to_numpy()

table_1 = {
    r'$H$': convert_to_string_with_decimal_number(H, 0),
    r'$M_{min}$': convert_to_string_with_decimal_number(M_min, 3),
    r'$M_{кр}$': convert_to_string_with_decimal_number(M_4, 3),
    r'$M_{max}$': convert_to_string_with_decimal_number(M_max, 3),
        }
print(pd.DataFrame(table_1).to_latex(escape=False, index=False))






