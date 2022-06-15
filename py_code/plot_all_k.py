import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import config
import re
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

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


def get_row(df, i):
    return df.iloc[i].to_numpy()


def find_row_and_column_by_value(data_frame, value):
    return np.where(data_frame == value)


def make_simple_plot(
    x, y, label_text, xlabel, ylabel, limit_x=None, limit_y=None, marker="o-"
):
    plt.plot(x, y, marker, label=label_text, linewidth=4, markersize=10)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    if limit_x:
        margin_5_per = (np.max(limit_x) * 5) / 100
        limit_x[-1] = limit_x[-1] + margin_5_per
        plt.xlim(limit_x)
    if limit_y:
        margin_5_per = (np.max(limit_y) * 5) / 100
        limit_y[-1] = limit_y[-1] + margin_5_per
        plt.ylim(limit_y)


def plot_from_arrays(alts, x_values, y_values, legend_name, x_label, y_label):
    markers = [
        "v",
        "^",
        "<",
        ">",
        "8",
        "s",
        "p",
        "P",
        "*",
        "h",
        "H",
        "+",
        "x",
        "X",
        "D",
    ]

    for i in range(0, len(alts)):
        H = get_row(alts, i)[0]
        y_row = get_row(y_values, i)
        x_row = get_row(x_values, i)
        make_simple_plot(
            x_row, y_row, legend_name % (H), x_label, y_label, marker=markers[i] + "-"
        )


def save_figure(save_path):
    plt.legend()
    plt.grid()
    plt.savefig(save_path, bbox_inches="tight")
    print(f"figure saved in {save_path}")
    plt.clf()


altitudes = pd.read_csv(config.PATH_DATA + config.FILE_H, header=None)
q = pd.read_csv(config.PATH_DATA + config.FILE_Q, header=None)
K_omega_z = pd.read_csv(config.PATH_DATA + config.FILE_K_OMEGA_Z, header=None)
K_theta = pd.read_csv(config.PATH_DATA + config.FILE_K_THETA, header=None)
K_H = pd.read_csv(config.PATH_DATA + config.FILE_K_H, header=None)
i_H = pd.read_csv(config.PATH_DATA + config.FILE_i_H, header=None)

q_global_max = np.max(q.max().to_numpy())
K_omega_z_global_max = np.max(K_omega_z.max().to_numpy())
K_theta_global_max = np.max(K_omega_z.max().to_numpy())

plot_from_arrays(
    altitudes,
    q,
    K_omega_z,
    "$H=%s$ м",
    "$q, [\\frac{кг}{м \\,с^2}$]",
    "$K_{\\omega_z}$",
)
fine_q = np.genfromtxt(config.PATH_DATA + "fine_q.csv", delimiter=",")
fine_K_omega_z = np.genfromtxt(config.PATH_DATA + "fine_K_omega_z.csv", delimiter=",")
plt.plot(fine_q, fine_K_omega_z, "ko--", label="$K_{\\omega_z}$ выбранное")
save_figure(config.PATH_SAVE + "K_omega_z_H_q.pgf")

plot_from_arrays(
    altitudes,
    q,
    K_theta,
    "$H=%s$ м",
    "$q, [\\frac{кг}{м \\,с^2}$]",
    "$K_{\\vartheta}$",
)
fine_K_theta = np.genfromtxt(config.PATH_DATA + "fine_K_theta.csv", delimiter=",")
plt.plot(fine_q, fine_K_theta, "ko--", label="$K_{\\vartheta}$ выбранное")
save_figure(config.PATH_SAVE + "K_theta_H_q.pgf")


plot_from_arrays(
    altitudes,
    q,
    K_H,
    "$H=%s$ м",
    "$q, [\\frac{кг}{м \\,с^2}$]",
    "$K_{H}$",
)
save_figure(config.PATH_SAVE + "K_H_H_q.pgf")


plot_from_arrays(
    altitudes,
    q,
    i_H,
    "$H=%s$ м",
    "$q, [\\frac{кг}{м \\,с^2}$]",
    "$i_{H}$",
)
save_figure(config.PATH_SAVE + "i_H_H_q.pgf")
