#!/bin/bash 

#SBATCH --job-name=MoS2-2H.pdos
#SBATCH --output=pdos.out
#SBATCH --error=pdos.err
#SBATCH --time=1:00:00
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --mem=4000
#SBATCH --ntasks-per-node=32

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

SYST=MoS2-2H

# needs the SCF charge density in ../out from 1-Relax
mpirun -np 32 $QE/pw.x < $SYST.nscf.pw > $SYST.nscf.pw.out
mpirun -np 32 $QE/projwfc.x < $SYST.pdos.in > $SYST.pdos.out
python plot_pdos.py
