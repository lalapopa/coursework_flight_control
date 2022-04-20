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

file_names = os.listdir(config.PATH_DATA+config.PATH_DATA_BODE)

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
    mag = mag[::-1]
    freq = freq[::-1]
    previous_mag = None  
    bw_freq = []

    find_positive = True
    find_negative = False 
    for i, f in enumerate(freq):
        previous_mag = mag[i]
        if find_positive:
            if previous_mag > 0:
                mag_int = interpolate.interp1d([previous_mag, mag[i-1]], [f, freq[i-1]])
                bw_freq.append(mag_int(0))
                find_negative = True 
                find_positive = False
        if find_negative:
            if previous_mag < 0:
                mag_int = interpolate.interp1d([previous_mag, mag[i-1]], [f, freq[i-1]])
                bw_freq.append(mag_int(0))
                find_negative = False 
                find_positive = True 
    if bw_freq:
        if len(bw_freq) == 1:
            return bw_freq[0]
        return bw_freq 
    else:
        return None
        

def check_phase_for_margin_plot(phase, freq, pm_freq):
    phase_values = []
    if all(pm_freq) == 0:
        return -180
    for i in pm_freq:
        phase_int = interpolate.interp1d(freq, phase, kind='linear')
        phase_values.append(phase_int(i))
    max_phase = max(phase_values) 
    if max_phase > 180:
        return 180
    else:
        return -180


def plot_margins(axs, g_m, g_f, p_m, p_f, horizontal_line=-180):
    if all(p_f) == 0:
        pass
    else:
        axs[1].axhline(horizontal_line, ls='--', color='k')
    main_color = axs[0].lines[-1].get_color()
    for i, phase_freq in enumerate(p_f):
        if phase_freq > 0:
            axs[1].plot([phase_freq, phase_freq], [horizontal_line, horizontal_line+p_m[i]], 'k')
            axs[1].plot(phase_freq, horizontal_line+p_m[i], 'o', linewidth=2, c=main_color)

    axs[0].axhline(0, ls='--', color='k')
    for i, gain_freq in enumerate(g_f):
        if gain_freq > 0:
            axs[0].plot([gain_freq, gain_freq], [-g_m[i], 0], 'k')
            axs[0].plot(gain_freq, -g_m[i], 'o', linewidth=2, c=main_color)


def set_plot_decoration(axs):
    axs[0].legend()
    for ax in axs:
        ax.grid()
        ax.set_xlim([10**-2, 10**3])
        ax.set_xlim([10**-2, 10**3])

def create_latex_table(column_M, column_bw, column_gain_m, column_phase_m):
    column_M = np.array(column_M)
    column_bw = np.array(column_bw)
    column_phase_m = np.array(column_phase_m)
    column_gain_m = np.array(column_gain_m)
    if len(column_bw.shape) == 1:
        rows = {
                r'$M$': column_M,
                r'$\omega_{ср}$, рад/с': column_bw,
                r'$\Delta Q$, дБ': column_gain_m,
                r'$\Delta L$, град.': column_phase_m,
                }
        df = pd.DataFrame(rows)
        print(df.to_latex(escape=False, index=False, float_format="%.3f"))
    else:
        df = pd.DataFrame()
        for i, mach in enumerate(column_M):
            midx = pd.MultiIndex(
                    levels=[[f"{mach}"], [f"{round(column_gain_m[i], 3)}", '']], codes=[[0, 0], [0, 1]]
                    )
            data = np.array([column_bw[i][::-1], column_phase_m[i]]).T
            df2 = pd.DataFrame(data, index=midx)
            df2.index.set_names([r'$M$', r'$\Delta Q$, дБ'], inplace=True)
            df2 = df2.rename(columns={0:r'$\omega_{ср}$, рад/с', 1:r'$\Delta L$, град.'})
            df = pd.concat([df, df2])

        print(df.to_latex(escape=False, float_format="%.3f"))


def filter_gain_phase_margins(gain_margin, gain_freq, phase_margin, phase_freq):
    if len(gain_margin) == 1 and len(phase_margin) == 1:
        return gain_margin, gain_freq, phase_margin, phase_freq
    for i, freq in enumerate(gain_freq):
        if freq == 0:
            gain_margin = np.delete(gain_margin, i)
            gain_freq = np.delete(gain_freq, i)
    return gain_margin, gain_freq, phase_margin, phase_freq

bode_names = BodeNames(sorted(file_names))
three_plots = 0
column_M = []
column_bw = []
column_gain_m = []
column_phase_m = []

fig, ax = plt.subplots(2, sharex=True)
for i, tf in enumerate(bode_names):
    print(f'open {tf["bode_values"]}')


    mag, phs, freq = get_bode_plot_data(config.PATH_DATA+config.PATH_DATA_BODE+tf['bode_values'])
    gain_margin, gain_freq, phase_margin, phase_freq = get_margins(
            config.PATH_DATA+config.PATH_DATA_BODE+tf['margin_values']
            )
    bandwidth = find_bandwidth_freq(mag, freq)
    gain_margin, gain_freq, phase_margin, phase_freq = filter_gain_phase_margins(gain_margin, gain_freq, phase_margin, phase_freq)
    
    column_M.append(f'{tf["mach"]}')
    column_bw.append(bandwidth)
    if len(gain_margin) == 1:
        column_gain_m.append(gain_margin[0])
    else:
        column_gain_m.append(gain_margin)

    if len(phase_margin) == 1: 
        if phase_margin[0] == -180 or phase_margin[0] == 0:
            column_phase_m.append('-')
        else:
            column_phase_m.append(phase_margin[0])
    else:
        column_phase_m.append(phase_margin)
        
    
    ax = plot_bode(ax, mag, phs, freq, f'$M={tf["mach"]}$')
    horizontal_line = check_phase_for_margin_plot(phs, freq, phase_freq)
    plot_margins(ax, gain_margin, gain_freq, phase_margin, phase_freq, horizontal_line)

    file_name_re = re.findall(r"(?<=W_)\w*(?=_H)", tf["bode_values"])[0] 
    file_name = f'{file_name_re}.pgf'

    if three_plots == 2:
        set_plot_decoration(ax)
        fig.savefig(config.PATH_SAVE+file_name)
        fig.clf()
        plt.close(fig)
        fig, ax = plt.subplots(2, sharex=True)
        create_latex_table(column_M, column_bw, column_gain_m, column_phase_m)
        three_plots = 0
        column_M = []
        column_bw = []
        column_gain_m = []
        column_phase_m = []
        
    else:
        three_plots += 1
