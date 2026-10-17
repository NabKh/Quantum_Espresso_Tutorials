#!/bin/bash

#SBATCH --job-name=mos2-hse
#SBATCH --output=hse.log
#SBATCH --error=hse.err
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

PREFIX=mos2

mpirun -np 32 $QE/pw.x -nk 4 -in $PREFIX.scf.in > $PREFIX.scf.out
