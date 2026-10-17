"""Plot the phonon dispersion of 2H-MoS2 from the output of matdyn.x.

Reads:
    mos2.freq.gp     path coordinate and frequencies in cm-1 (matdyn.x)
    mos2.matdyn.in   number of points between the corners of the path

Usage:
    python plot_dispersion.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
LABELS = [r"$\Gamma$", "M", "K", r"$\Gamma$", "A"]


def read_corners(path):
    """Return the row index of each corner of the path in mos2.freq.gp."""
    lines = path.read_text().splitlines()
    end = lines.index("/")  # end of the &input namelist
    rows = [line.split("!")[0].split() for line in lines[end + 1 :]]
    rows = [r for r in rows if r]
    steps = [int(r[3]) for r in rows[1:]]
    return np.concatenate([[0], np.cumsum(steps[:-1])])


def main():
    data = np.loadtxt(HERE / "mos2.freq.gp")
    q, freqs = data[:, 0], data[:, 1:]
    ticks = q[read_corners(HERE / "mos2.matdyn.in")]

    print(f"Lowest frequency: {freqs.min():.1f} cm-1")
    if freqs.min() < -5:
        print("Imaginary modes found: check the convergence of 2-scf and 3-ph.")

    fig, ax = plt.subplots(figsize=(4.5, 4))
    ax.plot(q, freqs, color="k", lw=0.8)
    for x in ticks:
        ax.axvline(x, color="0.6", lw=0.5)
    ax.axhline(0, color="0.6", lw=0.5)
    ax.set_xticks(ticks, LABELS)
    ax.set_xlim(q[0], q[-1])
    ax.set_ylabel(r"Frequency (cm$^{-1}$)")
    ax.set_title(r"2H-MoS$_2$, PBE+D3")
    fig.tight_layout()
    fig.savefig(HERE / "mos2_dispersion.png", dpi=300)
    fig.savefig(HERE / "mos2_dispersion.pdf")


if __name__ == "__main__":
    main()
