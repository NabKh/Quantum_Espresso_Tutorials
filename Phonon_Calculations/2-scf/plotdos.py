"""Plot the electronic density of states of 2H-MoS2.

Runs dos.x (it must be on your PATH) if mos2.dos does not exist yet, then
plots the DOS with the Fermi level read from the header of mos2.dos.

Usage:
    python plotdos.py
"""

import re
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DOS = HERE / "mos2.dos"

if not DOS.exists():
    with open(HERE / "mos2.dos.in") as stdin:
        subprocess.run(["dos.x"], stdin=stdin, cwd=HERE, check=True)

header = DOS.read_text().splitlines()[0]
efermi = float(re.search(r"EFermi\s*=\s*([-\d.]+)", header).group(1))
dos = np.loadtxt(DOS)

fig, ax = plt.subplots(figsize=(3, 6))
ax.plot(dos[:, 1], dos[:, 0] - efermi, lw=1.5)
ax.axhline(0, color="k", linestyle=":")
ax.set_xlim(0, 10)
ax.set_ylim(-7, 5)
ax.set_xlabel("DOS (states/eV)")
ax.set_ylabel(r"$E - E_\mathrm{F}$ (eV)")
fig.tight_layout()
fig.savefig(HERE / "mos2_dos.png", dpi=300)
plt.show()
