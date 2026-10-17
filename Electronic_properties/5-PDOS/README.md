# Projected density of states of 2H-MoS<sub>2</sub>

The total DOS shows how many states there are at each energy. The projected DOS (PDOS) also shows which atom and which orbital they come from. Here it tells you which orbitals form the top of the valence band and the bottom of the conduction band.

Only the input files are given. Run them yourself.

## Steps

```
5-PDOS/
├── MoS2-2H.nscf.pw    pw.x        non-self-consistent run on a dense k-mesh
├── MoS2-2H.pdos.in    projwfc.x   projection on atomic orbitals
└── plot_pdos.py                   total DOS and Mo d, Mo s, S p, S s
```

Run `1-Relax` first: the nscf run reads its charge density from `../out`. Then

```bash
sbatch run.sbatch      # pw.x (nscf), projwfc.x, then python plot_pdos.py
```

## The inputs

**nscf.** The charge density from the relaxation is kept fixed, and pw.x only computes eigenvalues on a denser 18×18×4 k-mesh. Compared with `2-Nscf`:

- `occupations = 'tetrahedra_opt'` uses the optimized tetrahedron method, which gives a smooth DOS without a smearing width to choose.
- `nbnd = 30` adds 12 empty bands so that the conduction band appears in the DOS.
- `verbosity = 'high'` makes pw.x print the eigenvalues at every k-point. `plot_pdos.py` needs them to find the band edges.

**projwfc.x** projects every Kohn–Sham state on the atomic orbitals stored in the pseudopotentials. It writes one file per atom and orbital, named `MoS2-2H.pdos.pdos_atm#N(El)_wfc#M(l)`, plus the total DOS in `MoS2-2H.pdos.pdos_tot`. In each file the first column is the energy in eV and the second is the summed (ldos) projected DOS.

## Reading the result

`plot_pdos.py` sums the PDOS over all atoms of the same element and puts the valence band maximum at 0 eV. With tetrahedra, pw.x prints a Fermi energy, which lies somewhere in the gap, so the script takes the band edges from the printed eigenvalues instead.

Check:

- The gap printed by `plot_pdos.py` should agree with the band structure from `4-plotbands`. If the two disagree, look at where each method finds the band edges.
- Look at which orbitals dominate just below 0 eV and just above the gap.
- Look at the top of `MoS2-2H.pdos.out`. projwfc.x prints the spilling parameter, which tells you how well the atomic orbitals describe the Kohn–Sham states. A small value means the projections can be trusted.

## Things to try

1. Split the Mo d channel by orbital. In the `wfc#3(d)` files, columns 3–7 are d<sub>z²</sub>, d<sub>zx</sub>, d<sub>zy</sub>, d<sub>x²−y²</sub>, d<sub>xy</sub> (see the orbital order in the [projwfc.x documentation](https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html)). Which of them form the valence band maximum at Γ?
2. Replace `tetrahedra_opt` with `smearing` and `degauss = 0.01`, then compare the shape of the DOS near the band edges.
3. Run the same steps on the PBE+D3 cell from `Phonon_Dispersion_D3/` and compare the gaps.
