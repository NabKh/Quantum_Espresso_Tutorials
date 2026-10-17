#!/bin/bash

#SBATCH --job-name=mos2-vc-relax
#SBATCH --output=vc-relax.log
#SBATCH --error=vc-relax.err
#SBATCH --time=2:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

PREFIX=mos2

mpirun -np 32 $QE/pw.x -in $PREFIX.vc-relax.in > $PREFIX.vc-relax.out
