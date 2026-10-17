# Band gap of 2H-MoS<sub>2</sub> with the HSE06 hybrid functional

Semilocal functionals such as PBE underestimate band gaps. Hybrid functionals mix in a fraction of exact (Fock) exchange and usually bring the gap much closer to experiment. HSE06 uses 25% exact exchange, screened at long range, and it is the most common choice for semiconductors.

This part runs the same structure twice, once with PBE and once with HSE06, and compares the gaps. Only the input files are given. Run them yourself.

## Steps

```
Hybrid_HSE06/
├── 1-scf-pbe/       pw.x   PBE reference
├── 2-scf-hse/       pw.x   HSE06 (input_dft = 'hse')
└── compare_gaps.py         prints both gaps
```

Both use the PBE+D3 cell from `Phonon_Dispersion_D3/1-vc-relax`. If you relaxed it yourself, copy your values of `celldm(1)`, `celldm(3)` and the S z coordinate. The geometry is kept fixed, so the difference between the two runs comes only from the functional.

```bash
cd 1-scf-pbe && sbatch run.sbatch
cd ../2-scf-hse && sbatch run.sbatch
cd .. && python compare_gaps.py
```

## The HSE06 input, line by line

- `input_dft = 'hse'` switches on HSE06. It overrides the PBE functional stored in the pseudopotential files; the PBE pseudopotentials are still used.
- `nqx1, nqx2, nqx3` set the q-grid for the exact exchange. A coarser q-grid than the k-grid saves a lot of time, but each q-grid number must divide the matching k-grid number (here 6 6 2 for k and 3 3 1 for q).
- `ecutfock` is the cutoff for the exact-exchange operator. Lowering it from the default (`ecutrho`, here 240 Ry) speeds up the run. Check that the gap does not change when you raise it.
- `nbnd = 22` adds empty bands. Without them `pw.x` computes only the occupied bands and cannot print the conduction band minimum.

`pw.x` first converges the PBE ground state, then switches on exact exchange and iterates again (the lines starting with `EXX:`). Compare the wall times at the end of the two outputs: the HSE run is far more expensive.

## Reading the result

With `occupations = 'fixed'` and empty bands, `pw.x` prints

```
highest occupied, lowest unoccupied level (ev):
```

near the end of the output. `compare_gaps.py` reads that line from both runs.

The gap is taken only over the k-points of the SCF grid. In the PBE band structure of `Electronic_properties/4-plotbands` the gap is indirect, from Γ to K, and both points are on the 6×6×2 grid; if the band edges of your structure fall between grid points, the grid gap is only an upper bound. A full HSE band structure along a path is usually obtained by Wannier interpolation (Wannier90).

## Things to try

1. Change `nqx1, nqx2, nqx3` to `6, 6, 2` (the full k-grid). How much does the gap change, and how much longer does it take?
2. Raise `ecutfock` to 240 Ry.
3. Increase the k-grid to 12×12×3 (keeping q at 3×3×1 or 6×6×1) and see whether the PBE and HSE gaps move.
4. Set `exx_fraction = 0.35` together with `input_dft = 'hse'` and watch how the gap depends on the amount of exact exchange.
