"""Plot the band structure of 2H-MoS2 from the output of bands.x.

Reads:
    MoS2-2H.bands.dat            band energies in eV along the path (bands.x)
    MoS2-2H.bands.bands.out      positions of the high-symmetry points (bands.x)
    ../3-Bands/MoS2-2H.bands.pw.out   number of electrons (pw.x)

Energies are shifted so that the valence band maximum is at 0 eV.

Usage:
    python plot_bands.py
"""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
LABELS = [r"$\Gamma$", "M", "K", r"$\Gamma$", "A", "L", "H", "A"]


def read_bands(path):
    """Return the path coordinate k (n_k) and energies in eV (n_bands x n_k).

    Reads the .dat file written by bands.x: a header with nbnd and nks, then
    for each k-point its Cartesian coordinates (2pi/a) followed by nbnd
    energies. The .gnu file of this run is in Ry, so it is not used here.
    """
    lines = path.read_text().splitlines()
    nbnd, nks = (int(n) for n in re.findall(r"\d+", lines[0]))
    values = np.array(" ".join(lines[1:]).split(), dtype=float)
    blocks = values.reshape(nks, 3 + nbnd)
    kpts, energies = blocks[:, :3], blocks[:, 3:].T
    steps = np.linalg.norm(np.diff(kpts, axis=0), axis=1)
    k = np.concatenate([[0.0], np.cumsum(steps)])
    return k, energies


def read_high_symmetry(path):
    """Return the x coordinates of the high-symmetry points."""
    pattern = r"high-symmetry point:.*x coordinate\s+([-\d.]+)"
    return [float(x) for x in re.findall(pattern, path.read_text())]


def read_nelec(path):
    match = re.search(r"number of electrons\s*=\s*([\d.]+)", path.read_text())
    return round(float(match.group(1)))


def main():
    k, energies = read_bands(HERE / "MoS2-2H.bands.dat")
    ticks = read_high_symmetry(HERE / "MoS2-2H.bands.bands.out")
    nocc = read_nelec(HERE.parent / "3-Bands" / "MoS2-2H.bands.pw.out") // 2

    # bands.x reorders bands by symmetry, which fails near some degeneracies;
    # sort the energies at each k-point instead
    levels = np.sort(energies, axis=0)
    vbm = levels[nocc - 1].max()
    cbm = levels[nocc].min()
    k_vbm = k[levels[nocc - 1].argmax()]
    k_cbm = k[levels[nocc].argmin()]
    print(f"VBM = {vbm:.3f} eV at x = {k_vbm:.3f}")
    print(f"CBM = {cbm:.3f} eV at x = {k_cbm:.3f}")
    print(f"Band gap (PBE) = {cbm - vbm:.3f} eV")

    fig, ax = plt.subplots(figsize=(4.5, 4))
    for band in levels:
        ax.plot(k, band - vbm, color="k", lw=0.8)
    for x in ticks:
        ax.axvline(x, color="0.6", lw=0.5)
    ax.axhline(0, color="tab:red", lw=0.6, ls="--")
    ax.set_xticks(ticks, LABELS[: len(ticks)])
    ax.set_xlim(ticks[0], ticks[-1])
    ax.set_ylim(-4, 4)
    ax.set_ylabel(r"$E - E_\mathrm{VBM}$ (eV)")
    ax.set_title(rf"2H-MoS$_2$, PBE, $E_g$ = {cbm - vbm:.2f} eV")
    fig.tight_layout()
    fig.savefig(HERE / "MoS2-2H_bands.png", dpi=300)
    fig.savefig(HERE / "MoS2-2H_bands.pdf")


if __name__ == "__main__":
    main()
