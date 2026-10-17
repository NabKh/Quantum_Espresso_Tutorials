# Quantum_Espresso_Tutorials

Step-by-step Quantum ESPRESSO inputs for bulk 2H-MoS<sub>2</sub> (6 atoms, hexagonal cell): structural relaxation, electronic band structure, density of states, and Γ-point phonons. Each step has its input file, the output it produced, and a SLURM script.

The newer parts (`Phonon_Dispersion_D3/`, `Hybrid_HSE06/`, `Electronic_properties/5-PDOS/`) are hands-on exercises: they give the inputs and explain each step, but not the outputs. Run them yourself and check your results against the notes in each README.

## Contents

```
Electronic_properties/
├── 1-Relax/       relax          ionic relaxation (pw.x)
├── 2-Nscf/        nscf           non-self-consistent run on a 12×12×12 k-mesh (pw.x)
├── 3-Bands/       bands          band structure on 113 k-points along a high-symmetry path (pw.x)
├── 4-plotbands/   bands.x        bands → MoS2-2H.bands.dat(.gnu), bands.xmgr, plot_bands.py
└── 5-PDOS/        nscf + projwfc.x  orbital-projected DOS (tetrahedra), plot_pdos.py
Phonon_Calculations/
├── 1-relax/       vc-relax       cell + ionic relaxation (pw.x)
├── 2-scf/         scf + dos.x    SCF on a 16×16×8 k-mesh, electronic DOS, plotdos.py
├── 3-phonon/      ph.x           phonons at Γ (DFPT) → mos2.dyn
└── 4-dynmat/      dynmat.x       Γ-point mode frequencies and eigenvectors (dynmat.axsf, dynmat.mold)
Phonon_Dispersion_D3/              full phonon dispersion with PBE+D3: vc-relax → scf + d3hess.x → ph.x on a q-grid → q2r.x → matdyn.x
Hybrid_HSE06/                      PBE vs HSE06 band gap on the same cell
pseudo/                            the two pseudopotentials used everywhere
```

See the README in each new folder for what every step does and what to check.

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

1. The pseudopotentials are in `pseudo/`, and every input points to it (`pseudo_dir = '../../pseudo'`). The `.sbatch` files find the QE executables with `command -v pw.x`, so load your QE module first, and adjust cores and time limits for your cluster.
2. Submit each step with `sbatch run.sbatch` (or `relax.sbatch`, `scf.sbatch`, …).
3. Plot the bands with `python plot_bands.py` in `4-plotbands/` (reads `MoS2-2H.bands.dat`, in eV), or use `bands.xmgr` (xmgrace). Note that `MoS2-2H.bands.dat.gnu` was written by an old `bands.x` in Ry.
4. Plot the DOS with `python plotdos.py` in `2-scf/`. It reads the Fermi energy from the header of `mos2.dos`.

## Known issues

Check these before using the old inputs as a reference:

- **Γ-point phonons are not converged.** `Phonon_Calculations/4-dynmat/mos2.dynmat.out` lists an imaginary mode at −105 cm<sup>−1</sup>. It stays after switching to the correct acoustic sum rule (below), so it comes from the phonon run itself: the SCF used `conv_thr = 1e-8`, and the cell has no van der Waals correction. `Phonon_Dispersion_D3/` shows a converged setup.
- **No van der Waals correction.** PBE alone does not bind the MoS<sub>2</sub> layers properly, so the c-axis is too long (about 14.9 Å in `Electronic_properties`). This also opens the band gap: `plot_bands.py` gives 1.52 eV (Γ → K) for that cell. `Phonon_Dispersion_D3/` and `Hybrid_HSE06/` use a PBE+D3 cell instead.

Fixed in the current version:

- `mos2.dynmat.in` used `asr = 'zero-dim'` (for molecules). It now uses `asr = 'crystal'`, and the outputs in `4-dynmat/` were regenerated.
- `1-Relax/run.sbatch` read a file name that did not exist; the input names in all scripts now match.
- The title line of `mos2.ph.in` said MoTe2.
