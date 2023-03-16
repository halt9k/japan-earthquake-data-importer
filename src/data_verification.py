from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import axes
import numpy as np

import scipy as sp
import scipy.fftpack

from jap_txt_parser import HEADER_SCALE_VAL


def add_histo(fname, axis_acel_data, limit):
    header_df, meas_df, _ = axis_acel_data  # type: pd.DataFrame, pd.DataFrame, _

    mean = meas_df[0].mean()
    print('Mean of ', fname, mean)

    scale_factor = header_df.loc[header_df[0] == HEADER_SCALE_VAL].iat[0, 1]
    ascel_vals = (meas_df[0] - meas_df[0].mean()).values * scale_factor

    minv, maxv = ascel_vals.min(), ascel_vals.max()
    print('Min, max ', minv, maxv)

    # bins = np.hstack((-np.inf,  np.arange(-500, 500, 2) * 0.0005, np.inf))
    # ax = meas_df[1].hist(bins=bins, histtype='step', stacked=True, fill=False, linewidth=0.3)  # type: axes.Axes
    # ax.set_ylim(top=limit)

    # meas_df[2] = sp.fftpack.fft(meas_df[1].values)
    # ax = meas_df[2].plot(linewidth=0.3)

    vals = sp.fftpack.fft(ascel_vals)
    n = len(vals)
    plt.plot(2.0 / n * np.abs(vals[0:n // 2]), linewidth=0.3)



def save_hists(arcs_data, limit):
    for arc_name, eq_data in arcs_data.items():
        for fname, axis_acel_data in eq_data.items():
            plt.figure(dpi=200)
            add_histo(fname, axis_acel_data, limit=limit)

            path = Path(arc_name).parent / Path(fname)
            # plt.title = path
            plt.figtext(0.5, 0.01, fname, wrap=True, horizontalalignment='center', fontsize=12)
            # plt.show()

            plt.savefig(str(path) + '.png')
            plt.close()


def save_data_verification_plots(arcs_data):
    # save_hists(arcs_data, limit=None)
    save_hists(arcs_data, limit=50)