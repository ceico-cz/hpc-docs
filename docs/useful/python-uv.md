---
title: "Using UV package manager with Python at Phoebe"
wikijs_updated: 2024-11-25
description: "TBF"
---

# Using UV package manager with Python at Phoebe

## Using UV python package manager

### howto 

Load modules providing MPI, gcc and friends, and our Python we selected arbitrarly
```
module load foss/2024a
module load Python/3.12.3-GCCcore-13.3.0
```

To make sure, we're not interfering with packages leftovers, we clean our local site-packages directory. Make sure there is nothing valuable.

```
rm ~/.local/lib/python3.12 -rf
```

Install the uv using pip:

```
python -m pip install uv
```

that's it :)

### run python within created uv _project_

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

### Install package inside of env

```
[jose@login1 example2]$ uv add pyyaml
Resolved 5 packages in 165ms
Prepared 1 package in 74ms
Installed 1 package in 33ms
 + pyyaml==6.0.2
[jose@login1 example2]$
```
