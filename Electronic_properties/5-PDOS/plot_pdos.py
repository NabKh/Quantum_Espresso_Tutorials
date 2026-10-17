"""Plot the total and orbital-projected DOS of 2H-MoS2 from projwfc.x.

Reads:
    MoS2-2H.pdos.pdos_tot                  total DOS (projwfc.x)
    MoS2-2H.pdos.pdos_atm#*(El)_wfc#*(l)   DOS projected on each atom and orbital
    MoS2-2H.nscf.pw.out                    eigenvalues, for the band edges (pw.x)

Energies are shifted so that the valence band maximum is at 0 eV.

Usage:
    python plot_pdos.py
"""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
PREFIX = "MoS2-2H.pdos"
CHANNELS = [("Mo", "d"), ("Mo", "s"), ("S", "p"), ("S", "s")]


def read_band_edges(path):
    """Band edges from the eigenvalues that pw.x prints at every k-point.

    With tetrahedra pw.x prints a Fermi energy, which lies somewhere in the gap,
    so the valence band maximum is taken from the eigenvalues instead.
    """
    text = path.read_text()
    nocc = round(
        float(re.search(r"number of electrons\s*=\s*([\d.]+)", text).group(1)) / 2
    )
    blocks = re.findall(
        r"bands \(ev\):\s*\n(.*?)\n\s*\n\s*(?:occupation|k =|the Fermi)",
        text,
        re.DOTALL,
    )
    energies = np.array(
        [[float(x) for x in re.findall(r"-?\d+\.\d+", b)] for b in blocks]
    )
    return energies[:, nocc - 1].max(), energies[:, nocc].min()


def summed_pdos(element, orbital):
    """Sum the projected DOS (column 2, ldos) over all atoms of one element."""
    files = sorted(HERE.glob(f"{PREFIX}.pdos_atm#*({element})_wfc#*({orbital})"))
    data = [np.loadtxt(f) for f in files]
    return data[0][:, 0], sum(d[:, 1] for d in data)


def main():
    vbm, cbm = read_band_edges(HERE / "MoS2-2H.nscf.pw.out")
    print(f"VBM = {vbm:.3f} eV, CBM = {cbm:.3f} eV, gap = {cbm - vbm:.3f} eV")

    total = np.loadtxt(HERE / f"{PREFIX}.pdos_tot")
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.fill_between(total[:, 0] - vbm, total[:, 1], color="0.85", label="Total")
    for element, orbital in CHANNELS:
        energy, dos = summed_pdos(element, orbital)
        ax.plot(energy - vbm, dos, lw=1, label=f"{element} {orbital}")
    ax.axvline(0, color="k", lw=0.6, ls="--")
    ax.set_xlim(-7, 5)
    ax.set_ylim(0, None)
    ax.set_xlabel(r"$E - E_\mathrm{VBM}$ (eV)")
    ax.set_ylabel("DOS (states/eV/cell)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / "MoS2-2H_pdos.png", dpi=300)
    fig.savefig(HERE / "MoS2-2H_pdos.pdf")


if __name__ == "__main__":
    main()
