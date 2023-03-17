from pathlib import Path

import matplotlib.pyplot as plt
import obspy.io.nied.knet as knet
from obspy.core import read
from obspy.core import Trace
from obspy.core.trace import Stats
from obspy.signal.trigger import classic_sta_lta
import typing

from obspy.core import read
from obspy.signal.trigger import plot_trigger


def plot_trace(tr: Trace):
    tr.data = (tr.data - tr.data.mean()) * tr.meta.calib*1000

    st = tr.stats  # type: Stats
    df = st.sampling_rate
    cft = classic_sta_lta(tr.data, int(5 * df), int(10 * df))
    plot_trigger(tr, cft, 1.5, 0.5, show=False)
    plt.savefig(tr.id + '.png')
    plt.close()


def main():
    file_paths = list(Path().glob("*/*.*[1-2]"))

    # st = st.select(component="Z")
    for path in file_paths:
        tr = read(path).traces[0]  # type: Trace
        tr.meta.location = Path(path).parts[0]
        plot_trace(tr)


main()