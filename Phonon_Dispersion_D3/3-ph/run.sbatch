#!/bin/bash

#SBATCH --job-name=mos2-ph
#SBATCH --output=ph.log
#SBATCH --error=ph.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

PREFIX=mos2

rm -rf out _ph0
cp -r ../2-scf/out .
mpirun -np 64 $QE/ph.x -nk 4 -in $PREFIX.ph.in > $PREFIX.ph.out
