# autoparse

Set of wrappers for python.re that allow for more intelligible regular expressions syntax.


### Installation using Conda

The most direct way to install the code is through the conda package manager.
If you have conda installed, simply run the following command in whichever
environment you choose:
```
conda install -c auto-mech mess
```
If you do not have conda, it can be installed using the shell script
`debug/install-conda.sh`.

### Building from source using Conda environment for dependencies

To build the code from source for development or debugging purposes, first
create a conda environment with the necessary dependencies as follows:
```
conda env create -f environment.yml
```
which will create the `mess-env` environment.
You can then activate the environment and build the code as follows:
```
conda activate mess-env
bash debug/build.sh
```
To put the MESS executables in your path, you can then run
```
. debug/fake-install.sh
```

### Building from source without Conda

Run the setup.py script

## Reference

See Y. Georgievskii, J. A. Miller, M. P. Burke, and S. J. Klippenstein,
Reformulation and Solution of the Master Equation for Multiple-Well Chemical
Reactions, J. Phys. Chem. A, 117, 12146-12154 (2013).

## Acknowledgment

This work was supported by the U.S. Department of Energy, Office of Basic Energy
Sciences, Division of Chemical Sciences, Geosciences, and Biosciences under DOE
Contract Number DE-AC02-06CH11357 as well as the Exascale Computing Project
(ECP), Project Number: 17-SC-20-SC.  The ECP is a collaborative effort of two
DOE organizations, the Office of Science and the National Nuclear Security
Administration, responsible for the planning and preparation of a capable
exascale ecosystem including software, applications, hardware, advanced system
engineering, and early test bed platforms to support the nation's exascale
computing imperative. 

## Notice

Authors:
Andreas V. Copan
Kevin B. Moore III
