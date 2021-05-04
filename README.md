# AUTOIO
[//]: # (Badges)
[![CircleCI](https://circleci.com/gh/snelliott/autoio_new/tree/dev.svg?style=shield)](https://circleci.com/gh/snelliott/autoio_new/tree/dev)
Andreas V. Copan, Kevin B. Moore III, Sarah N. Elliott, and Stephen J. Klippenstein

Input writing, output parsing, and job submission tools created as part of the AutoMech package. This repository contains the following python packages: elstruct, autoparse, autoio, and autorun.

## ELSTRUCT
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/elstruct/badges/version.svg)](https://anaconda.org/auto-mech/elstruct)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/elstruct/badges/platforms.svg)](https://anaconda.org/auto-mech/elstruct)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/elstruct/badges/installer/conda.svg)](https://conda.anaconda.org/auto-mech/elstruct)
### Installation
```python
>>> conda install elstruct -c auto-mech
```
### Description
The elstruct package handles input writing and output reading for electronic structure jobs. Current modules available:
- Geometry optimization: GAUSSIAN (v09, v16), PSI4, ORCA, QCHEM
- Frequency calculation:
- VPT2 anharmonic analysis:

### Usage
Our pytest tests serve as an example for building filesystems

## AUTOPARSE
[//]: # (Badges)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autoparse/badges/version.svg)](https://anaconda.org/auto-mech/autoparse)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autoparse/badges/platforms.svg)](https://anaconda.org/auto-mech/autoparse)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autoparse/badges/installer/conda.svg)](https://conda.anaconda.org/auto-mech/autoparse)
### Installation
```python
>>> conda install autoparse -c auto-mech
```
### Description
Autoparse provides a user-friendly interface for regex calls and has built specific series of calls for parsing strings of interest to the AutoMech suite

### Usage
Our pytest tests serve as an example for building filesystems

## AUTOIO
[//]: # (Badges)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autoio/badges/version.svg)](https://anaconda.org/auto-mech/autoio)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autoio/badges/platforms.svg)](https://anaconda.org/auto-mech/autoio)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autoio/badges/installer/conda.svg)](https://conda.anaconda.org/auto-mech/autoio)
### Installation
```python
>>> conda install autoio -c auto-mech
```
### Description
AutoIO generates the input and reads the output for  C++ and Fortran codes used by the AutoMech suite.  These codes include:
Distributed in AutoMech
- MESS: conda install, github link, paper, authorlist
- THERM: conda install, github link, authorlist
- 
External Codes
- CHEMKIN: paper, authorlist
- PAC99
- 
### Usage
Our pytest tests serve as an example for building filesystems

## AUTORUN
[//]: # (Badges)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autorun/badges/version.svg)](https://anaconda.org/auto-mech/autorun)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autorun/badges/platforms.svg)](https://anaconda.org/auto-mech/autorun)
[![Anaconda-Server Badge](https://anaconda.org/auto-mech/autorun/badges/installer/conda.svg)](https://conda.anaconda.org/auto-mech/autorun)
### Installation
```python
>>> conda install autorun -c auto-mech
```
### Description
AutoRUN submits jobs and extracts relevant output through calls to autoio for  C++ and Fortran codes used by the AutoMech suite.  These codes include:
Distributed in AutoMech
- MESS: conda install, github link, paper, authorlist
- THERM: conda install, github link, authorlist
- 
External Codes
- CHEMKIN: paper, authorlist
- PAC99
- 
### Usage
Our pytest tests serve as an example for building filesystems
