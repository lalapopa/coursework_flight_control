import os 
import re
import config
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.simplefilter("ignore", FutureWarning)

def pgf_setting():
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

def split_nonlinear_linear(file_names):
    nonlinear = []
    linear = []
    variants = []
    for name in file_names:
        variants.append(re.findall(r'DD_\d\.\d*', name)[0])
    unique_variant = list(set(variants))
    if len(unique_variant) != 2:
        raise ValueError
    print(unique_variant)
    for name in file_names:
        if re.search(unique_variant[0], name):
            linear.append(name)
            continue 
        if re.search(unique_variant[-1], name):
            nonlinear.append(name)
            continue 
    return nonlinear, linear

def get_data_from_csv(file_name):
    df = pd.read_csv(file_name)
    time = df['time'].to_numpy() 
    value = df['value'].to_numpy() 
    return (time, value) 

def from_name_get_mach_number(file_name):
    mach_pattern = r"0_[\d]{4}"
    raw_mach_number = re.findall(mach_pattern, file_name)
    return float(re.sub(r"_", '.', raw_mach_number[0]))

def validate_name(file_name, params):
    for name in params:
        re_name = f"(?<=_){name}(?=_DD)"
        if re.search(re_name, file_name):
            return name
    return False

def remove_Delta_H_names(file_names):
    Delta_H_names = []
    another_names = []

    for name in file_names:
        if re.search(r"(?<=_)Delta_H(?=_DD)", name): 
            Delta_H_names.append(name)
        elif re.search(r"(?<=_)Delta_H_target(?=_DD)", name):
            continue 
        else:
            another_names.append(name)
    return another_names, Delta_H_names

def get_input_signal(file_names):
    for name in file_names:
        if re.search(r"(?<=nonlinear_model_)Delta_H_target(?=_DD)", name):
            return name
       

pgf_setting()
params =[
        "omega_z", "Delta_H_target", "Delta_H", "delta_elevator", "theta", "Delta_H"
        ]

plot_labels_y = {
        'theta' : r"$\vartheta,\ ??????$",
        'omega_z' : r"$\omega_z,\ ??????/??$",
        'delta_elevator' : r"$\delta_{??},\ ??????$",
        'Delta_H_target' : r"$\Delta H_{??????},\ ??$",
        'Delta_H' :  r"$\Delta H,\ ??$",
        }
plot_labels_x = {
        't' : r"$t,\ ??$",
        }

file_names = sorted(os.listdir(config.PATH_DATA+config.PATH_DATA_MODEL_DD))
print(file_names)
file_names = [i for i in file_names if '_stats_' not in i]
nonlinear_names, linear_names = split_nonlinear_linear(file_names)
input_signal_name = get_input_signal(file_names)
linear_names, Delta_H_names_linear = remove_Delta_H_names(linear_names)
nonlinear_names, Delta_H_names_nonlinear = remove_Delta_H_names(nonlinear_names)

fig, axes = plt.subplots(1)
three_plots = 0
for i, val in enumerate(linear_names):
    print(f'#{i} | {val} | {nonlinear_names[i]}')
    time_l, value_linear = get_data_from_csv(config.PATH_DATA+config.PATH_DATA_MODEL_DD+val)
    time_nl, value_nonlinear = get_data_from_csv(config.PATH_DATA+config.PATH_DATA_MODEL_DD+nonlinear_names[i])

    mach_number = from_name_get_mach_number(val)
    axes.plot(time_nl, value_nonlinear, label=r'???????????? ?????? $\dot{\delta}_{{??}_{max}}=15 \frac{????????.}{??????.}$')
    axes.plot(time_l, value_linear, '-.', label=r'???????????? ?????? $\dot{\delta}_{{??}_{max}}=60 \frac{????????.}{??????.}$')

    if three_plots == 0:
        validated_name = validate_name(val, params)
        plt.legend()
        plt.grid()
        if validated_name == 'delta_elevator':
            ax2 = fig.add_axes([0.465, 0.36, 0.4, 0.3])
            ax2.plot(time_nl,value_nonlinear)
            ax2.plot(time_l, value_linear, '--' )
            ax2.set_xlim([0, 3])
            ax2.grid()
        axes.set(ylabel=plot_labels_y[validated_name])
        axes.set(xlabel=plot_labels_x['t'])
        save_path = config.PATH_SAVE+f"model_DD_{validated_name}.pgf"
        plt.savefig(config.PATH_SAVE+f"model_DD_{validated_name}.pgf")
        print(f'saved to {save_path}')
        fig.clf()
        plt.close(fig)
        fig, axes = plt.subplots(1)
        three_plots = 0
    else:
        three_plots += 0


fig, axes = plt.subplots(1)
for i, name in enumerate(Delta_H_names_linear):

    time_l, value_linear = get_data_from_csv(config.PATH_DATA+config.PATH_DATA_MODEL_DD+name)
    time_nl, value_nonlinear = get_data_from_csv(config.PATH_DATA+config.PATH_DATA_MODEL_DD+Delta_H_names_nonlinear[i])

    mach_number = from_name_get_mach_number(name)
    axes.plot(time_nl, value_nonlinear, label=r'???????????? ?????? $\dot{\delta}_{{??}_{max}}=15 \frac{????????.}{??????.}$')
    axes.plot(time_l, value_linear, '-.', label=r'???????????? ?????? $\dot{\delta}_{{??}_{max}}=60 \frac{????????.}{??????.}$')
    param_name = validate_name(name, params)

time_input, value_input = get_data_from_csv(config.PATH_DATA+config.PATH_DATA_MODEL_DD+input_signal_name)
axes.plot(time_input, value_input,':' ,label=r'$\Delta H_{??????}$')
plt.legend()
plt.grid()
axes.set(ylabel=plot_labels_y[param_name])
axes.set(xlabel=plot_labels_x['t'])
save_path = config.PATH_SAVE+f"model_DD_{param_name}.pgf"
plt.savefig(config.PATH_SAVE+f"model_DD_{param_name}.pgf")



