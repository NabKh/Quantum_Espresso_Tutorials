#!/bin/bash

#SBATCH --job-name=mos2-q2r
#SBATCH --output=q2r.log
#SBATCH --error=q2r.err
#SBATCH --time=0:10:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

PREFIX=mos2

cp ../3-ph/$PREFIX.dyn* .
$QE/q2r.x -in $PREFIX.q2r.in > $PREFIX.q2r.out
