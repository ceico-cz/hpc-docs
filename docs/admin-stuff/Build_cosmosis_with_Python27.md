---
title: "Build cosmosis with python 2.7 in conda"
wikijs_updated: 2024-02-27
tags:
  - "app-specific cosmosis"
---

# Build cosmosis with python 2.7 in conda

## Create conda environment

(as user)

this ensures

* gcc is fixed to version 9.5.0 (newer fails to build cosmosis)
* python is fixed to version 2.7 - specific to this particular "release" of cosmosis

```
conda create -n cosmosis_py27_gcc95_v2 python=2.7 gxx=9.5.0 gcc=9.5.0 openmpi mpi4py gsl cfitsio fftw lapack gfortran astropy cfitsio emcee future minuit2 pyyaml numpy scipy configparser backports openblas
```

## Patch cosmosis setup file

make sure that `COSMOSIS_SRC_DIR` is set properly to root of cosmosis source code tree.

```
(cosmosis_py27_gcc95_v2) [jose@login1 cosmosis_EMU]$ cat setup-my-cosmosis
# setup cosmosis:

export COSMOSIS_SRC_DIR=/home/jose/projects/2024_02_26__cosmosis/cosmosis_EMU

#The gnu science library
export GSL_INC=${CONDA_PREFIX}/include
export GSL_LIB=${CONDA_PREFIX}/lib

#The cfitsio FITS library
export CFITSIO_INC=${CONDA_PREFIX}/include
export CFITSIO_LIB=${CONDA_PREFIX}/lib

#The fftw3 Fourier transform library
#export FFTW_LIBRARY=$EBROOTFFTW/lib
#export FFTW_INCLUDE_DIR=$EBROOTFFTW/include

#The lapack linear algebra package
export LAPACK_LINK="-L${CONDA_PREFIX}/lib -llapack -lblas"

export LD_LIBRARY_PATH=${CONDA_PREFIX}/lib:${COSMOSIS_SRC_DIR}/cosmosis/datablock/:${COSMOSIS_SRC_DIR}/cosmosis-standard-library/likelihood/planck2015/plc-2.0/lib/:${LD_LIBRARY_PATH}

export PYTHONPATH=${COSMOSIS_SRC_DIR}:${PYTHONPATH}
export PATH=${COSMOSIS_SRC_DIR}/bin:${PATH}
(cosmosis_py27_gcc95_v2) [jose@login1 cosmosis_EMU]$
```

## Insert -march=native in compiler opt

ensure that in `config/compilers.mk` is `-march=native` in non-debug config:

```
ifeq (1,$(COSMOSIS_DEBUG))
COMMON_FLAGS=-O0 -g -fPIC  -fno-omit-frame-pointer
else
COMMON_FLAGS=-O3 -g -fPIC -march=native
endif
```

## Activate env and build cosmosis

```
conda activate cosmosis_py27_gcc95_v2
source setup-my-cosmosis
make
```

## Create batch file

```
#!/bin/bash
#SBATCH --job-name=testbed
#SBATCH --partition=cpu_int
#SBATCH --ntasks=145
#SBATCH --time=12:00:00
#SBATCH --exclusive

cd /home/jose/projects/2024_02_26__cosmosis/cosmosis_EMU

# activate conda:
source /etc/profile.d/conda.sh
conda activate cosmosis_py27_gcc9

# test if we see right gcc
which gcc

source setup-my-cosmosis

# we use mpi inside of conda so we need to use mpirun:
mpirun /home/examples/mpi_hello_world/a.out

```
