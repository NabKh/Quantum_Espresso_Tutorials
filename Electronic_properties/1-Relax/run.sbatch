#!/bin/bash 

#SBATCH --job-name=2H-MoS2.relax
#SBATCH --output=relax.out
#SBATCH --error=relax.err
#SBATCH --time=1:00:00
#SBATCH --qos=normal
#SBATCH --nodes=2
#SBATCH --mem=4000
#SBATCH --ntasks-per-node=16

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

SYST=2H-MoS2
TYPE=relax
CALC=pw

mpirun -np 32 $QE/$CALC.x < $SYST.$TYPE.$CALC > MoS2-2H.$TYPE.$CALC.out
