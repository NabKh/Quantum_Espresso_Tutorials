# Phonon dispersion of 2H-MoS<sub>2</sub> with PBE+D3

This part goes from the relaxed structure to the full phonon dispersion along Γ–M–K–Γ–A. It uses density-functional perturbation theory (DFPT) in `ph.x`. Compared with `Phonon_Calculations/`, which computes phonons at Γ only, it adds:

- a van der Waals correction (Grimme D3), which holds the MoS<sub>2</sub> layers together at the right distance;
- phonons on a full grid of q-points, Fourier-interpolated to any point in the Brillouin zone;
- the correct acoustic sum rule for a bulk crystal.

Only the input files are given. Run each step yourself and look at the outputs as you go.

## Steps

```
Phonon_Dispersion_D3/
├── 1-vc-relax/   pw.x       relax the cell and the atoms with PBE+D3
├── 2-scf/        pw.x       ground state on the relaxed cell
│                 d3hess.x   D3 contribution to the force constants
├── 3-ph/         ph.x       dynamical matrices on a 6×6×2 q-grid
├── 4-q2r/        q2r.x      real-space interatomic force constants
└── 5-matdyn/     matdyn.x   frequencies along the path, plot_dispersion.py
```

Run them in order. Each step uses files from the step before it, and the `run.sbatch` scripts copy them for you. Adjust the number of cores and the time limits for your cluster. The pseudopotentials are in `../pseudo`.

### 1-vc-relax

The starting cell is close to experiment (a = 3.16 Å, c = 12.30 Å). `cell_dofree = 'ibrav'` keeps the cell hexagonal while a and c change.

Phonons are computed at zero force, so the structure has to be relaxed with exactly the same settings (functional, cutoff, k-points, D3) as the phonon run.

When it finishes, take the new cell and positions from the block between `Begin final coordinates` and `End final coordinates` at the end of `mos2.vc-relax.out`:

- `celldm(1)` = 5.9716 × the first number of `CELL_PARAMETERS` (the value of alat used in this run)
- `celldm(3)` = third diagonal element / first diagonal element of `CELL_PARAMETERS`
- the S z coordinate from `ATOMIC_POSITIONS`

Put them in `2-scf/mos2.scf.in`. The values already there come from our own run of this input; check that yours agree.

### 2-scf

This is a normal SCF with a much tighter threshold (`conv_thr = 1e-12`). The phonon calculation is the response of this ground state, so any noise in it shows up as wrong frequencies, often as small imaginary modes near Γ.

`d3hess.x` then computes the second derivatives of the D3 energy and writes `out/mos2.hess`. `ph.x` stops with an error if this file is missing.

### 3-ph

`ldisp = .true.` asks for phonons on a uniform 6×6×2 grid. `ph.x` uses symmetry to reduce it to the irreducible q-points and writes one dynamical matrix per point (`mos2.dyn1`, `mos2.dyn2`, …). `mos2.dyn0` lists the grid.

`epsil = .true.` also gives the dielectric tensor and the Born effective charges at Γ, which `q2r.x` and `matdyn.x` use for the long-range (LO–TO) part.

This is the expensive step. In our test, ph.x at Γ alone took about 13 times as long as the SCF in 2-scf, and q-points away from Γ have less symmetry and cost more. Run it on a cluster. `-nk 4` splits the k-points over 4 groups of processes, which usually speeds up `ph.x`. If the job stops, add `recover = .true.` to `&inputph` and resubmit; it continues from where it stopped.

### 4-q2r

`q2r.x` Fourier-transforms the dynamical matrices on the q-grid into interatomic force constants in real space (`mos2.fc`). The 6×6×2 grid sets how far apart two atoms can be and still have their interaction included.

### 5-matdyn

`matdyn.x` builds the dynamical matrix at any q from `mos2.fc` and diagonalises it. With `q_in_band_form = .true.`, each line gives a corner of the path (in units of 2π/a) and the number of points to the next corner. The A point is (0, 0, a/2c), so it changes if your c/a is different.

`asr = 'crystal'` enforces the acoustic sum rule: three modes at exactly 0 cm<sup>−1</sup> at Γ. Do not use `'zero-dim'`; that is for molecules.

Then run `python plot_dispersion.py` (needs NumPy and Matplotlib) to get `mos2_dispersion.png` and `.pdf`.

## What to check

- **No imaginary frequencies.** Negative values in `mos2.freq.gp` are imaginary modes. Small ones (a few cm<sup>−1</sup>) near Γ usually point to a loose SCF threshold or a coarse q-grid. Large ones mean the structure is not at a minimum.
- **Three acoustic branches go to zero at Γ**, and only three.
- **The frequencies at Γ** from `3-ph/mos2.ph.out` (the first q-point) should match those from `matdyn.x` at Γ.
- **Compare with experiment.** The Raman-active E<sup>1</sup><sub>2g</sub> (in-plane) and A<sub>1g</sub> (out-of-plane) modes of MoS<sub>2</sub> are both measured near 400 cm<sup>−1</sup> (C. Lee *et al.*, ACS Nano **4**, 2695 (2010), [doi:10.1021/nn1003937](https://doi.org/10.1021/nn1003937)). Find the matching modes at Γ in your output and read the measured bulk values from that paper.

## Why D3, and why without the three-body term

PBE alone gives almost no binding between MoS<sub>2</sub> layers, so a PBE `vc-relax` makes c much too long (compare `Phonon_Calculations/1-relax`). D3 adds the missing dispersion attraction.

`d3hess.x` and `ph.x` implement only the two-body part of D3. The three-body term (on by default in `pw.x`) is switched off with `dftd3_threebody = .false.` in every step. Using the same setting everywhere matters more than the small change in the lattice constants.

## Things to try

1. Repeat 3–5 with a 4×4×1 q-grid and compare the curves. Which branches change, and along which direction?
2. Run 1-vc-relax without `vdw_corr`. How much does c change? What happens to the low-frequency modes along Γ–A?
3. Change `conv_thr` in 2-scf to `1e-8`, rerun 3-ph at Γ only (`ldisp = .false.` and `0.0 0.0 0.0` on the last line), and compare the frequencies.
4. Converge `ecutwfc` and the k-mesh before you trust any of this: increase each until the total energy changes by less than 1 mRy per cell and the pressure by less than 1 kbar.
