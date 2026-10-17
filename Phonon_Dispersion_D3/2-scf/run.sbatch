#!/bin/bash

#SBATCH --job-name=mos2-scf
#SBATCH --output=scf.log
#SBATCH --error=scf.err
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

PREFIX=mos2

# 1. ground state on the relaxed cell
mpirun -np 32 $QE/pw.x -in $PREFIX.scf.in > $PREFIX.scf.out

# 2. second derivatives of the D3 energy, written to out/$PREFIX.hess (read by ph.x)
mpirun -np 32 $QE/d3hess.x -in $PREFIX.d3hess.in > $PREFIX.d3hess.out
