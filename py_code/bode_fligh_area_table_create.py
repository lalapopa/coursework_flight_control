import pandas as pd 
import numpy as np
import re
import config

def format_latex_table(latex_string):
    re_hline = r'\\hline'
    number_of_column = len(list(re.findall(r"(?<={)r*(?=})", latex_string))[0])
    print(number_of_column)
    new_prefix = '|'+'c|'*number_of_column
    latex_string = re.sub(r'(?<={)r*(?=})', new_prefix, latex_string)
    latex_string = re.sub(r'(\\bottomrule)|(\\midrule)|(\\toprule)', re_hline, latex_string)
    return latex_string

def save_string_to_file(input_data, file_name):
    with open(file_name, "w") as f:
        f.write(input_data)

df = pd.read_csv(config.PATH_DATA+config.PATH_DATA_BODE + config.FILE_BODE_FLIGHT_AREA)
df.rename(columns={'H': '$H,\ м$', 'q': r'$q,\ \frac{кг}{м\,с^2}$', 'mach': '$M$'}, inplace=True)
formated_latex_table = format_latex_table(df.to_latex(escape=False, index=False, float_format="%.4f" ))
save_string_to_file(formated_latex_table, config.PATH_REPORT+"bode_flight_area_stats.tex")




