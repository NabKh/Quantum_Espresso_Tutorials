#!/bin/bash

#SBATCH --job-name=mos2-matdyn
#SBATCH --output=matdyn.log
#SBATCH --error=matdyn.err
#SBATCH --time=0:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

PREFIX=mos2

cp ../4-q2r/$PREFIX.fc .
$QE/matdyn.x -in $PREFIX.matdyn.in > $PREFIX.matdyn.out
python plot_dispersion.py
