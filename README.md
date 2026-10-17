# Quantum_Espresso_Tutorials

Step-by-step Quantum ESPRESSO inputs for bulk 2H-MoS<sub>2</sub> (6 atoms, hexagonal cell): structural relaxation, electronic band structure, density of states, and Γ-point phonons. Each step has its input file, the output it produced, and a SLURM script.

## Contents

```
Electronic_properties/
├── 1-Relax/       relax          ionic relaxation (pw.x)
├── 2-Nscf/        nscf           non-self-consistent run on a 12×12×12 k-mesh (pw.x)
├── 3-Bands/       bands          band structure on 113 k-points along a high-symmetry path (pw.x)
└── 4-plotbands/   bands.x        bands → MoS2-2H.bands.dat(.gnu) and bands.xmgr for plotting
Phonon_Calculations/
├── 1-relax/       vc-relax       cell + ionic relaxation (pw.x)
├── 2-scf/         scf + dos.x    SCF on a 16×16×8 k-mesh, electronic DOS, plotdos.py
├── 3-phonon/      ph.x           phonons at Γ (DFPT) → mos2.dyn
└── 4-dynmat/      dynmat.x       Γ-point mode frequencies and eigenvectors (dynmat.axsf, dynmat.mold)
```

## Settings

| | Electronic_properties | Phonon_Calculations |
|---|---|---|
| Functional / pseudopotentials | PBE, FHI norm-conserving (`S.pbe-mt_fhi.UPF`, `Mo.pbe-mt_fhi.UPF`) | same |
| `ecutwfc` | 37 Ry | 50 Ry (`ecutrho` 250 Ry in SCF) |
| k-mesh | 12×12×2 (relax), 12×12×12 (nscf) | 12×12×6 (vc-relax), 16×16×8 (scf) |
| Smearing | 0.005 Ry | Fermi–Dirac, 0.005 Ry |
| van der Waals correction | none (`vdw_corr` is commented out) | none |
| QE version in the outputs | 5.2.0 | 6.2 |

## Running

Run the steps in order inside each folder. Every step reads the `out/` directory written by the step before it.

1. Change `pseudo_dir` in each input and the executable path in each `.sbatch` file to match your installation.
2. Submit each step with `sbatch run.sbatch` (or `relax.sbatch`, `scf.sbatch`, …).
3. Plot the bands from `4-plotbands/MoS2-2H.bands.dat.gnu` (gnuplot) or `bands.xmgr` (xmgrace).
4. Plot the DOS with `python plotdos.py` in `2-scf/`. The Fermi energy in the script (7.634 eV) matches `mos2.pw.out`.

## Known issues

Check these before using the inputs as a reference:

- **Γ-point phonons are not converged.** `4-dynmat/mos2.dynmat.out` lists an imaginary mode at −105 cm<sup>−1</sup>. The SCF used `conv_thr = 1e-8`, and phonons usually need tighter settings (e.g. `conv_thr ≈ 1e-12`, a converged cutoff and k-mesh).
- **Wrong acoustic sum rule for a bulk crystal.** `mos2.dynmat.in` uses `asr = 'zero-dim'`, which is meant for molecules and removes 6 modes (translations and rotations). Bulk MoS<sub>2</sub> has only 3 acoustic modes. Use `asr = 'crystal'`.
- **No van der Waals correction.** PBE alone does not bind the MoS<sub>2</sub> layers properly, so the interlayer distance and c-axis from `vc-relax` are unreliable. Use e.g. `vdw_corr = 'grimme-d3'`.
- **Input names don't match `1-Relax/run.sbatch`.** The script reads `-2H-MoS2.relax.pw.in`, but the input file is `2H-MoS2.relax.pw`.
- `mos2.ph.in` starts with the title line "MoTe2 Phonon calculation", although the system is MoS<sub>2</sub>.
