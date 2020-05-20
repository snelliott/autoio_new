# autoparse

Set of wrappers for python.re that allow for more intelligible regular expressions syntax.

### Installation using Conda

The most direct way to install the code is through the conda package manager.
If you have conda installed,  
(1) activate an environment you wish to use to run autoparse in, and  
(2) run the install command:
```
conda install -c auto-mech autoparse
```
If you do not have conda, it can be installed using the shell script
`debug/install-conda.sh`.

### Building from source using Conda environment for dependencies

To build the code from source for development or debugging purposes, first
create a conda environment with the necessary dependencies as follows:
```
conda env create -f environment.yml
```
which will create the `autoparse-env` environment.
You can then activate the environment and build the code as follows:
```
conda activt
```

### Building from source without Conda

Run the setup.py script
