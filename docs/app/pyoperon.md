---
title: "Pyoperon in conda at Phoebe"
wikijs_updated: 2025-08-12
description: "This guide details how to set up and install pyoperon on Phoebe using a clean Conda environment."
tags:
  - "app-specific"
  - "conda"
  - "operon"
  - "pyoperon"
---

# Pyoperon in conda at Phoebe

!!! info "Note"
    **Note:** This guide expects a **clean shell environment. Do not run it inside Jupyter Notebooks or environments enriched with preloaded modules or dependencies.**

Tested on: August 6, 2025


## Build pyoperon and its dependencies

### 1.1 Clone pyoperon from the Upstream Repository

```
git clone https://github.com/heal-research/pyoperon.git
cd pyoperon
```

### 1.2 Activate Conda and Create Environment

##### Optional tweaks to `environment.yml`:

- Use a stable version: `clangxx==19.1.7` instead of a cutting-edge version.
- To prepare for openMPI later, you may add:

```yaml
- ucx
- libpmix==5.0.8
```

📄 example `environment.yaml` can be found [here](https://gist.github.com/jose-d/aaeefc937a82d237a830a7acd11e13a6).

```
module load Miniforge3
# this is alternative way to activate conda without modifying user configuration..:
source ${EBROOTMINIFORGE3}/etc/profile.d/conda.sh

conda env create -f environment.yml
conda activate pyoperon
```

### 1.3 Configure Clang as the Compiler

```
export CC=${CONDA_PREFIX}/bin/clang
export CXX=${CONDA_PREFIX}/bin/clang++
```

### 1.4 Download Site-Specific Dependency Script and Run It

```
wget https://gist.githubusercontent.com/jose-d/9db74a1283eba9fbadf73d2d029ad505/raw/4aaa3044909779675c57135f41cd6b35101522bb/dependencies.sh --output-document=./script/dependencies.sh
chmod +x ./script/dependencies.sh 
./script/dependencies.sh
```

✅ This step might take some time. Warnings are expected, but no critical errors should occur.

### 1.5 Install pyoperon

```
pip install .
```

### 1.6 Test the Installation

Because the local directory shares a name with the module, avoid testing from within the project folder:

```bash
mkdir mytest
cd mytest
python
```

then test inside Python

```python

>>> from pyoperon.sklearn import SymbolicRegressor
>>>
```
If no errors appear, the installation was successful!

## 2 🚀 (Optional) Install and Run with OpenMPI

### 2.1 install openmpi from source

🛠️ To ensure compatibility, you'll build **OpenMPI** and **mpi4py** within the Conda environment you created earlier.

Get script from [here](https://gist.github.com/jose-d/079c16c9bf767b243d1375c4267f4988) and run it within the conda environment created in previous steps. This will take several minutes:


```bash
wget https://gist.githubusercontent.com/jose-d/079c16c9bf767b243d1375c4267f4988/raw/d7b916da17e5e6d03c1b6d5c6eaef40895488eaf/install_ompi.sh --output-document=./install_ompi.sh
chmod +x ./install_ompi.sh
./install_ompi.sh
```

### 2.2 install mpi4py from source

Once OpenMPI is built and available in your environment:

```bash
python -m pip install --no-binary=mpi4py mpi4py
```

This ensures mpi4py is compiled against your custom OpenMPI build.


## 3 Example batch job using software built above

```
#!/bin/bash
#SBATCH --job-name=operon_testcase
#SBATCH --time=00:33:33
#SBATCH --partition=cpu
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=64

echo "sbatch-INFO: start of job"
echo "sbatch-INFO: nodes: ${SLURM_JOB_NODELIST}"
echo "sbatch-INFO: system: ${SLURM_CLUSTER_NAME}"

module load Miniforge3
source ${EBROOTMINIFORGE3}/etc/profile.d/conda.sh
# here make sure you load the right enb
conda activate pyoperon_mpi
cd /home/jose/projects/pyoperon_in_micromamba/pyoperon
mpirun python ./hello_world.py



echo "sbatch-INFO: we're done"
date
```
