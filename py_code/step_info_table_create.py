import pandas as pd 
import numpy as np
import os 

import config

data = config.PATH_DATA_MODEL 

def return_linear_nonlinear_names(file_names):
    linear = []
    nonlinear = []
    for f in file_names:
        if 'nonlinear_' in f:
            nonlinear.append(f)
        if 'linear_' in f:
            linear.append(f)
    return linear[0], nonlinear[0]



file_names = sorted(os.listdir(config.PATH_DATA+data))
file_names = [i for i in file_names if '_stats_' in i] 
linear_data_name, nonlinear_data_name = return_linear_nonlinear_names(file_names)

df_lin = pd.read_csv(config.PATH_DATA+data+linear_data_name)
df_nonlin = pd.read_csv(config.PATH_DATA+data+nonlinear_data_name)

settling_time_lin = np.unique(df_lin['SettlingTime'].to_numpy())[0]
settling_time_nonlin = np.unique(df_nonlin['SettlingTime'].to_numpy())[0]

overshoot_lin = np.unique(df_lin['Overshoot'].to_numpy())[0]
overshoot_nonlin = np.unique(df_nonlin['Overshoot'].to_numpy())[0]


data = np.array([[settling_time_lin, settling_time_nonlin], [overshoot_lin, overshoot_nonlin]])
df = pd.DataFrame(data, index=[r'$t_{рег},\ с$', r'$\sigma,\ \%$']).rename(columns={0:'Линейная модель', 1: 'Нелинейная модель'})
print(df.to_latex(escape=False, float_format="%.2f"))




