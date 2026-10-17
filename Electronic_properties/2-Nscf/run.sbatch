#!/bin/bash 

#SBATCH --job-name=MoS2-2H.nscf
#SBATCH --output=nscf.out
#SBATCH --error=nscf.err
#SBATCH --time=1:00:00
#SBATCH --qos=normal
#SBATCH --nodes=2
#SBATCH --mem=4000
#SBATCH --ntasks-per-node=16

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

SYST=MoS2-2H
TYPE=nscf
CALC=pw

mpirun -np 32 $QE/$CALC.x < $SYST.$TYPE.$CALC > $SYST.$TYPE.$CALC.out
