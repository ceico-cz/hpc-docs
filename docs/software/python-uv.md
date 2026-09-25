---
title: "Using the uv package manager with Python on Phoebe"
wikijs_updated: 2024-11-25
description: "Install uv and manage Python projects with it on Phoebe"
---

# Using the uv package manager with Python on Phoebe

## Using the uv Python package manager

### Install uv

Load modules providing MPI, gcc and friends, and our Python we selected arbitrarly
```
module load foss/2024a
module load Python/3.12.3-GCCcore-13.3.0
```

Packages you installed earlier with `pip install --user` for the same Python version (in
`~/.local/lib/python3.12`) can interfere with uv environments. Check what is there:

```
python -m pip list --user
```

and remove only what you no longer need with `python -m pip uninstall <package>`.

Install the uv using pip:

```
python -m pip install uv
```

that's it :)

### Create a uv _project_

```
mkdir ~/example
cd ~/example
uv init
```

This creates `pyproject.toml` and a few starter files. uv creates the project's virtual
environment in `.venv` the first time you run or add something.

### Run Python in a uv _project_

```
[jose@login1 example]$ uv run python
Python 3.12.3 (main, Aug 29 2024, 16:11:54) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import ruff
>>> import mpi4py
>>> quit()
[jose@login1 example]$ which uv
~/.local/bin/uv
[jose@login1 example]$ uv run which python
/home/jose/example/.venv/bin/python
[jose@login1 example]$ uv run which gcc
/cvmfs/2024a.phoebe.lan/software/GCCcore/13.3.0/bin/gcc
[jose@login1 example]$ uv run which mpirun
/cvmfs/2024a.phoebe.lan/software/OpenMPI/5.0.3-GCC-13.3.0/bin/mpirun
[jose@login1 example]$
```

### Install a package into the environment

```
[jose@login1 example2]$ uv add pyyaml
Resolved 5 packages in 165ms
Prepared 1 package in 74ms
Installed 1 package in 33ms
 + pyyaml==6.0.2
[jose@login1 example2]$
```
