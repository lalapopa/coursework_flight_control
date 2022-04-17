import os 
import re
import config
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
from scipy import interpolate
import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.simplefilter("ignore", FutureWarning)

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

file_names = os.listdir(config.PATH_DATA_BODE_FOLDER)

class BodeNames:
    def __init__(self, names):
        self.names = names
    def __iter__(self):
        tf_names = ['W_theta_ol_H', 'W_theta_H', 'W_altitude_H', 'W_altitude_ol_H', 'W_core_damp_ol_H']
        for re_trigger in tf_names:
            r = re.compile(re_trigger)
            transfer_functions_names= list(filter(r.match, self.names))
            for tf in transfer_functions_names:
                if self.__is_stats_file(tf):
                    continue
                mach_number = self.__get_mach_number(tf)
                stats_file = re.sub(r'\.', '_stats.', tf)
                
                yield {
                        'bode_values': tf,
                        'margin_values': stats_file,
                        'mach': mach_number,
                        }

    def __get_mach_number(self, name):
        mach_pattern = r"0_[\d]{4}"
        raw_mach_number = re.findall(mach_pattern, name)
        return float(re.sub(r"_", '.', raw_mach_number[0]))

    def __is_stats_file(self, name):
        return re.search(r'_stats', name)


def get_bode_plot_data(file_name):
    df = pd.read_csv(file_name)
    mag = df['mag'].to_numpy() 
    phs = df['phs'].to_numpy() 
    freq = df['freq'].to_numpy() 
    return (mag, phs, freq) 

def plot_bode(ax, mag, phase, freq, label_text):
    ax[0].plot(freq, mag, label=label_text)
    ax[0].set(ylabel='Амплитуда, [дБ]')
    ax[1].plot(freq, phase, label=label_text)
    ax[1].set(ylabel='Фаза, [град.]')
    ax[0].set_xscale('log')
    ax[1].set_xscale('log')
    return ax

def get_margins(file_name):
    df = pd.read_csv(file_name)
    gain_margins = df['gain_m'].to_numpy()
    gain_freq = df['freq_gain'].to_numpy()
    phase_margins = df['phase_m'].to_numpy()
    phase_freq = df['freq_phase'].to_numpy()
    index_inf_values = np.where(gain_margins==np.Inf)

    gain_margins = np.delete(gain_margins, index_inf_values)
    gain_freq = np.delete(gain_freq, index_inf_values)
    phase_margins = np.delete(phase_margins, index_inf_values)
    phase_freq = np.delete(phase_freq, index_inf_values)
    return [gain_margins.astype('float64'), gain_freq.astype('float64'), phase_margins.astype('float64'), phase_freq.astype('float64')]

def find_bandwidth_freq(mag, freq):
    interp = interpolate.interp1d(mag, freq, kind = "linear")
    try:
        return interp(0)
    except ValueError:
        return None

def plot_margins(axs, g_m, g_f, p_m, p_f):
    main_color = axs[0].lines[-1].get_color()
    for i, phase_freq in enumerate(p_f):
        if phase_freq > 0:
            axs[1].axhline(-180, ls='--', color='k')
            axs[1].plot([phase_freq, phase_freq], [-180, -180+p_m[i]], 'k')
            axs[1].plot(phase_freq, -180+p_m[i], 'o', linewidth=2, c=main_color)

    for i, gain_freq in enumerate(g_f):
        if gain_freq > 0:
            axs[0].axhline(0, ls='--', color='k')
            axs[0].plot([gain_freq, gain_freq], [-g_m[i], 0], 'k')
            axs[0].plot(gain_freq, -g_m[i], 'o', linewidth=2, c=main_color)


def set_plot_decoration(axs):
    axs[0].legend()
    for ax in axs:
        ax.grid()
        ax.set_xlim([10**-2, 10**3])
        ax.set_xlim([10**-2, 10**3])



bode_names = BodeNames(file_names)

three_plots = 0
column_M = []
column_bw = []
column_gain_m = []
column_phase_m = []

fig, ax = plt.subplots(2, sharex=True)
for i, tf in enumerate(bode_names):
    print(f'open {tf["bode_values"]}')


    mag, phs, freq = get_bode_plot_data(config.PATH_DATA_BODE_FOLDER+tf['bode_values'])
    gain_margin, gain_freq, phase_margin, phase_freq = get_margins(
            config.PATH_DATA_BODE_FOLDER+tf['margin_values']
            )
    try:
        bandwidth = str(np.format_float_positional(find_bandwidth_freq(mag, freq), precision=3))
    except TypeError:
        bandwidth = '-'

    column_M.append(f'{tf["mach"]}')
    column_bw.append(bandwidth)
    column_gain_m.append(gain_margin[0])
    if phase_margin[0] == -180 or phase_margin[0] == 0:
        column_phase_m.append('-')
    else:
        column_phase_m.append(phase_margin[0])
        
    
    ax = plot_bode(ax, mag, phs, freq, f'$M={tf["mach"]}$')
    plot_margins(ax, gain_margin, gain_freq, phase_margin, phase_freq)

    file_name_re = re.findall(r"(?<=W_)\w*(?=_H)", tf["bode_values"])[0] 
    file_name = f'{file_name_re}.pgf'

    if three_plots == 2:
        set_plot_decoration(ax)
        fig.savefig(config.PATH_SAVE_FOLDER+file_name)
        fig.clf()
        plt.close(fig)
        fig, ax = plt.subplots(2, sharex=True)
        rows = {
                r'M': column_M,
                r'$\omega_{ср}$, рад/с': column_bw,
                r'$\Delta Q$, дБ': column_gain_m,
                r'$\Delta L$, град.': column_phase_m,
                }
        df = pd.DataFrame(rows)
        print(df.to_latex(escape=False, index=False, float_format="%.3f"))

        three_plots = 0
        column_M = []
        column_bw = []
        column_gain_m = []
        column_phase_m = []
        
    else:
        three_plots += 1
    

