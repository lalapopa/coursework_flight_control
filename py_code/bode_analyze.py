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
        "font.size": 14,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "axes.labelsize": 14,
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

file_names = os.listdir(config.PATH_DATA + config.PATH_DATA_BODE)


class BodeNames:
    def __init__(self, names):
        self.names = names

    def __iter__(self):
        tf_names = [
            "W_theta_ol_H",
            "W_theta_H",
            "W_altitude_H",
            "W_altitude_ol_H",
            "W_core_damp_ol_H",
        ]
        for re_trigger in tf_names:
            r = re.compile(re_trigger)
            transfer_functions_names = self.__sort_by_mach(
                list(filter(r.match, self.names))
            )
            for tf in transfer_functions_names:
                if self.__is_stats_file(tf):
                    continue
                mach_number = self.__get_mach_number(tf)
                stats_file = re.sub(r"\.", "_stats.", tf)
                yield {
                    "bode_values": tf,
                    "margin_values": stats_file,
                    "mach": mach_number,
                }

    def __sort_by_mach(self, names):
        mach_number = {}
        for i, name in enumerate(names):
            mach_value = self.__get_mach_number(name)
            mach_number[i] = mach_value
        sorted_mach = {
            w: mach_number[w] for w in sorted(mach_number, key=mach_number.get)
        }
        index_sorted_mach = list(sorted_mach.keys())
        return [names[i] for i in index_sorted_mach]

    def __get_mach_number(self, name):
        mach_pattern = r"0_[\d]{4}"
        raw_mach_number = re.findall(mach_pattern, name)
        return float(re.sub(r"_", ".", raw_mach_number[0]))

    def __is_stats_file(self, name):
        return re.search(r"_stats", name)

    @staticmethod
    def get_bode_type_name(name):
        tf_names = [
            "W_theta_ol_H",
            "W_theta_H",
            "W_altitude_H",
            "W_altitude_ol_H",
            "W_core_damp_ol_H",
        ]
        for tf_name in tf_names:
            if tf_name in name:
                return tf_name
        return "No_name"


def get_bode_plot_data(file_name):
    df = pd.read_csv(file_name)
    mag = df["mag"].to_numpy()
    phs = df["phs"].to_numpy()
    freq = df["freq"].to_numpy()
    return (mag, phs, freq)


def plot_bode(ax, mag, phase, freq, label_text, color_hex):
    ax[0].plot(freq, mag, label=label_text, color=color_hex)
    ax[0].set(ylabel="Амплитуда, [дБ]")
    ax[1].plot(freq, phase, label=label_text, color=color_hex)
    ax[1].set(ylabel="Фаза, [град.]")
    ax[1].set(xlabel="Частота, [рад/с]")
    ax[0].set_xscale("log")
    ax[1].set_xscale("log")
    return ax


def get_margins(file_name):
    df = pd.read_csv(file_name)
    gain_margins = df["gain_m"].to_numpy()
    gain_freq = df["freq_gain"].to_numpy()
    phase_margins = df["phase_m"].to_numpy()
    phase_freq = df["freq_phase"].to_numpy()

    index_inf_values_gain = np.where(gain_margins == np.Inf)
    index_inf_values_phase = np.where(phase_margins == np.Inf)

    gain_margins = np.delete(gain_margins, index_inf_values_gain)
    gain_freq = np.delete(gain_freq, index_inf_values_gain)
    phase_margins = np.delete(phase_margins, index_inf_values_phase)
    phase_freq = np.delete(phase_freq, index_inf_values_phase)
    return [
        gain_margins.astype("float64"),
        gain_freq.astype("float64"),
        phase_margins.astype("float64"),
        phase_freq.astype("float64"),
    ]


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
                mag_int = interpolate.interp1d(
                    [previous_mag, mag[i - 1]], [f, freq[i - 1]]
                )
                bw_freq.append(mag_int(0))
                find_negative = True
                find_positive = False
        if find_negative:
            if previous_mag < 0:
                mag_int = interpolate.interp1d(
                    [previous_mag, mag[i - 1]], [f, freq[i - 1]]
                )
                bw_freq.append(mag_int(0))
                find_negative = False
                find_positive = True
    if bw_freq:
        if len(bw_freq) == 1:
            return bw_freq[0]
        return bw_freq[-1]
    else:
        return "-"


def check_phase_for_margin_plot(phase, freq, pm_freq):
    avg_phase = calculate_avg(phase)
    if -20 < avg_phase < 200:
        return 180
    else:
        return -180


def calculate_avg(array):
    max_value = max(array)
    min_value = min(array)
    return (max_value + min_value) / 2


def plot_margins(axs, g_m, g_f, p_m, p_f, horizontal_line=-180):
    print(f"g_m plot= {g_m}, g_f plot= {g_f}, p_m plot= {p_m}, p_f plot= {p_f}")

    if p_f == 0:
        pass
    else:
        axs[1].axhline(horizontal_line, ls="--", color="k", linewidth=1)

    main_color = axs[0].lines[-1].get_color()

    if p_f > 0:
        axs[1].plot([p_f, p_f], [horizontal_line, horizontal_line + p_m], "k")
        axs[1].plot(p_f, horizontal_line + p_m, "o", linewidth=2, c=main_color)

    axs[0].axhline(0, ls="--", color="k", linewidth=1)
    if g_f > 0:
        axs[0].plot([g_f, g_f], [-g_m, 0], "k")
        axs[0].plot(g_f, -g_m, "o", linewidth=2, c=main_color)


def set_plot_decoration(axs):
    axs[0].legend()
    for ax in axs:
        ax.grid(True, which="minor", linestyle="--", linewidth=0.25)
        ax.grid(True, which="major")
        ax.set_xlim([10**-2, 10**3])
        ax.set_xlim([10**-2, 10**3])


def create_latex_table(column_M, column_bw, column_gain_m, column_phase_m):
    column_M = np.array(column_M)
    column_bw = np.array(column_bw)
    column_phase_m = np.array(column_phase_m)
    column_gain_m = np.array(column_gain_m)
    if len(column_bw.shape) == 1:
        rows = {
            r"$M$": column_M,
            r"$\omega_{ср}$, рад/с": column_bw,
            r"$\Delta Q$, дБ": column_gain_m,
            r"$\Delta L$, град.": column_phase_m,
        }
        df = pd.DataFrame(rows)

    else:
        df = pd.DataFrame()
        for i, mach in enumerate(column_M):
            midx = pd.MultiIndex(
                levels=[[f"{mach}"], [f"{round(column_gain_m[i], 3)}", ""]],
                codes=[[0, 0], [0, 1]],
            )
            data = np.array([column_bw[i][::-1], column_phase_m[i]]).T
            df2 = pd.DataFrame(data, index=midx)
            df2.index.set_names([r"$M$", r"$\Delta Q$, дБ"], inplace=True)
            df2 = df2.rename(
                columns={0: r"$\omega_{ср}$, рад/с", 1: r"$\Delta L$, град."}
            )
            df = pd.concat([df, df2])
        print(df.to_latex(escape=False, float_format="%.3f"))
    return format_latex_table(
        df.to_latex(escape=False, index=False, float_format="%.3f")
    )


def format_latex_table(latex_string):
    re_hline = r"\\hline"
    number_of_column = len(list(re.findall(r"(?<={)[lr]*(?=})", latex_string))[0])
    print(number_of_column)
    new_prefix = "|" + "c|" * number_of_column
    latex_string = re.sub(r"(?<={)[lr]*(?=})", new_prefix, latex_string)
    latex_string = re.sub(
        r"(\\bottomrule)|(\\midrule)|(\\toprule)", re_hline, latex_string
    )
    return latex_string


def save_string_to_file(input_data, file_name):
    with open(file_name, "w") as f:
        f.write(input_data)


def filter_gain_phase_margins(gain_margin, gain_freq, phase_margin, phase_freq):
    print("=" * 10, "MARGINS IN FILTER", "=" * 10)

    print(
        f"g_m plot= {gain_margin}, g_f plot= {gain_freq}, p_m plot= {phase_margin}, p_f plot= {phase_freq}"
    )
    print("=" * 25)

    if len(gain_margin) == 1 and len(phase_margin) == 1:
        if phase_margin[0] == -180:
            phase_margin = ["-"]
        return gain_margin[0], gain_freq[0], phase_margin[0], phase_freq[0]
    else:
        max_gf_index = np.unique(np.where(gain_freq == np.max(gain_freq)))[0]
        max_pf_index = np.unique(np.where(phase_freq == np.max(phase_freq)))[0]
        return [
            gain_margin[max_gf_index],
            gain_freq[max_gf_index],
            phase_margin[max_pf_index],
            phase_freq[max_pf_index],
        ]


bode_names = BodeNames(sorted(file_names))
three_plots = 0
column_M = []
column_bw = []
column_gain_m = []
column_phase_m = []

fig, ax = plt.subplots(2, sharex=True)
color_sequence = [
    "#525252",
    "#969696",
    "#cccccc",
]

for i, tf in enumerate(bode_names):
    print(f'open {tf["bode_values"]}')
    mag, phs, freq = get_bode_plot_data(
        config.PATH_DATA + config.PATH_DATA_BODE + tf["bode_values"]
    )
    gain_margin, gain_freq, phase_margin, phase_freq = get_margins(
        config.PATH_DATA + config.PATH_DATA_BODE + tf["margin_values"]
    )
    bandwidth = find_bandwidth_freq(mag, freq)
    gain_margin, gain_freq, phase_margin, phase_freq = filter_gain_phase_margins(
        gain_margin, gain_freq, phase_margin, phase_freq
    )
    column_M.append(f'{tf["mach"]}')
    column_bw.append(bandwidth)
    column_gain_m.append(gain_margin)
    column_phase_m.append(phase_margin)

    ax = plot_bode(ax, mag, phs, freq, f'$M={tf["mach"]}$', color_sequence[three_plots])
    horizontal_line = check_phase_for_margin_plot(phs, freq, phase_freq)
    plot_margins(ax, gain_margin, gain_freq, phase_margin, phase_freq, horizontal_line)

    file_name_re = re.findall(r"(?<=W_)\w*(?=_H)", tf["bode_values"])[0]
    file_name = f"{file_name_re}.pgf"

    if three_plots == 2:
        set_plot_decoration(ax)
        fig.savefig(config.PATH_SAVE + file_name)
        fig.clf()
        plt.close(fig)
        fig, ax = plt.subplots(2, sharex=True)

        latex_table = create_latex_table(
            column_M, column_bw, column_gain_m, column_phase_m
        )
        save_string_to_file(
            latex_table,
            config.PATH_REPORT
            + f'{bode_names.get_bode_type_name(tf["bode_values"])}.tex',
        )

        three_plots = 0
        column_M = []
        column_bw = []
        column_gain_m = []
        column_phase_m = []

    else:
        three_plots += 1
