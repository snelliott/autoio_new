#!/bin/sh

# Set current working directory
CWD=$(pwd)

# Set host
HOST=b456

# Load Molpro
module load molpro/2015.1_170920
MOLPROEXE=$(which molpro.exe)

# Set Molpro library directory
MOLPRO_LIB=/soft/molpro/2015.1_170920/bebop/molprop_2015_1_linux_x86_64_i8/lib/

# Add MRCC to the PATH to run this as a module
export PATH=/lcrc/project/PACC/brossdh/mrcc:$PATH

# Set the Molpro scratch directory
SCRDIR=/scratch/$USER

# Set runtime options for MPI
MPI_OPTIONS="-n 4 -ppn 4 -hosts $HOST"

# Set runtime options for Molpro
MOLPRO_OPTIONS="--nouse-logfile --no-xml-output -L $MOLPRO_LIB -d $SCRDIR -I $SCRDIR -W $SCRDIR -o $CWD/output.dat"

# Run the molpro executable
mpirun $MPI_OPTIONS $MOLPROEXE $MOLPRO_OPTIONS $CWD/input.dat >& /dev/null &


