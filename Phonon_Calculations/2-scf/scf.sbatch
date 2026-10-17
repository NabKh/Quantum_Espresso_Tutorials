#!/bin/bash 

#SBATCH --job-name=mos2-scf
#SBATCH --output=espresso.out
#SBATCH --error=espresso.err
#SBATCH --time=48:00:00
#SBATCH --qos=normal
#SBATCH --nodes=4
#SBATCH --mem=64000
#SBATCH --ntasks-per-node=16

PREFIX=mos2

mpirun -np 64 pw.x < $PREFIX.pw.in > $PREFIX.pw.out

