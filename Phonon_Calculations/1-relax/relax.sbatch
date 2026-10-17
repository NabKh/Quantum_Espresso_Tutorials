#!/bin/bash 

#SBATCH --job-name=mos2-relax
#SBATCH --output=espresso.out
#SBATCH --error=espresso.err
#SBATCH --time=48:00:00
#SBATCH --qos=normal
#SBATCH --nodes=8
#SBATCH --mem=64000
#SBATCH --ntasks-per-node=16

PREFIX=mos2

#rm -rf *out
mpirun -np 128 pw.x < $PREFIX.pw.in > $PREFIX.pw.out
