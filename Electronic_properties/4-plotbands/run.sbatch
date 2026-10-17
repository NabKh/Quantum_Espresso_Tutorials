#!/bin/bash

# Note: this calculation can be run in serial and does not require SLURM (sbatch)

QE=$(dirname "$(command -v pw.x)")   # folder with the QE executables: load your QE module first

SYST=MoS2-2H
TYPE=bands
CALC=bands

$QE/$CALC.x < $SYST.$TYPE.$CALC.in > $SYST.$TYPE.$CALC.out
