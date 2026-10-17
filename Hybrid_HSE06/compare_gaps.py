"""Compare the PBE and HSE06 band gaps of 2H-MoS2.

Reads the band edges printed by pw.x in 1-scf-pbe/mos2.scf.out and
2-scf-hse/mos2.scf.out. The gap is taken on the k-points of the SCF grid
only, so it is exact only if the band edges fall on grid points.

Usage:
    python compare_gaps.py
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERN = r"highest occupied, lowest unoccupied level \(ev\):\s+([-\d.]+)\s+([-\d.]+)"


def band_edges(path):
    vbm, cbm = (float(x) for x in re.findall(PATTERN, path.read_text())[-1])
    return vbm, cbm


for label, folder in [("PBE", "1-scf-pbe"), ("HSE06", "2-scf-hse")]:
    vbm, cbm = band_edges(HERE / folder / "mos2.scf.out")
    print(
        f"{label:6s} VBM = {vbm:7.3f} eV   CBM = {cbm:7.3f} eV   gap = {cbm - vbm:.3f} eV"
    )
