---
title: "Using Lmod software modules"
wikijs_updated: 2023-11-15
---

# Using Lmod software modules

Lmod (Lua-based Modules) sets up your environment (paths and variables) for the software you
choose. Most compilers, libraries and applications on Phoebe are installed centrally and
loaded as modules. Phoebe and Koios have different module trees: see
[Phoebe](#phoebe) and [Koios](#koios) below. Koios and the Phoebe GPU nodes use
[EESSI](eessi.md).

## Where modules come from

### Phoebe

Modules are grouped into stacks. Each numbered stack is built with one
[EasyBuild](https://docs.easybuild.io/) toolchain generation; `foss/2024a`, for example, is GCC
13.3 with OpenMPI, FlexiBLAS, FFTW and ScaLAPACK. Modules from different stacks don't mix: load
one `foss` toolchain and modules built with it.

| Stack | Location | Toolchain |
| --- | --- | --- |
| `2026a` | `/cvmfs/2026a.phoebe.lan` | `foss/2026.1` (GCC 15.2), `lfoss/2026.1` |
| `2025a` | `/cvmfs/2025a.phoebe.lan` | `foss/2025a` (GCC 14.2) |
| `2024a` | `/cvmfs/2024a.phoebe.lan` | `foss/2024a` (GCC 13.3) |
| `2023a` | `/cvmfs/2023a.phoebe.lan` | `foss/2023a` (GCC 12.3) |
| `system` | `/cvmfs/system.phoebe.lan` | none: CUDA, Miniforge3, Mathematica, MATLAB, Julia, VTune |

On Phoebe, all stacks are available on the login node and on the Rocky Linux 8 compute nodes.

### Phoebe GPU nodes (Rocky Linux 10)

The GPU nodes `gpu1` and `gpu2` (partition `rocky10`) have none of the stacks above: no module
tree is loaded there by default. Use the [EESSI software stack](eessi.md), which also has CUDA
and cuDNN modules, or the NVIDIA HPC SDK modules described in
[GPU jobs](../compute/gpu-jobs.md#software).

For new work, use the newest stack that has what you need.

### Koios

Koios has no module tree of its own: all modules come from the [EESSI software stack](eessi.md),
on the login node `koios1.fzu.cz` and on all compute and GPU nodes. No modules are available
until you start EESSI, in each shell and at the start of each job script:

```
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
```

After that, `module avail`, `module spider` and `module load` work as described below. EESSI has
the `foss` toolchains (`foss/2024a` to `foss/2025b` in version 2025.06), Python with
`SciPy-bundle`, HDF5, GSL, CFITSIO and much more.

The former Koios tree `/cvmfs/c9.phoebe.lan` has been retired together with Rocky Linux 9 on the
login node. Programs and Python environments built with its modules need to be rebuilt with EESSI
modules. A few of its modules have no EESSI counterpart (`HEALPix`, `PFFT`, `VTune`); build them
yourself with an EESSI toolchain or ask the administrator.

Koios has **no** `system` stack: no Miniforge3 or Mathematica modules. For conda, install
Miniforge3 into your home directory (see [conda on Koios](conda.md#on-koios)).

## Search for available modules

`module avail` lists every module you can load, stack by stack. `module -t avail` prints one
module per line, which is easier to search. On the login node:

```
[jose@login1 ~]$ module -t avail 2>&1 | grep -i '^python'
Python-bundle-PyPI/
Python-bundle-PyPI/2023.06-GCCcore-12.3.0
Python/
Python/3.11.3-GCCcore-12.3.0
Python-bundle-PyPI/
Python-bundle-PyPI/2024.06-GCCcore-13.3.0
Python/
Python/3.10.14-GCCcore-13.3.0-bare
Python/3.11.9-GCCcore-13.3.0-bare
Python/3.12.3-GCCcore-13.3.0
Python/
Python/3.13.1-GCCcore-14.2.0
Python/
Python/3.14.2-GCCcore-15.2.0
```

## Use `module spider` for information or search

`module spider` finds a module in any stack and describes it:

```
[jose@login1 ~]$ module spider Mathematica

----------------------------------------------------------------------------
  Mathematica:
----------------------------------------------------------------------------
    Description:
      Mathematica is a computational software program used in many
      scientific, engineering, mathematical and computing fields.

     Versions:
        Mathematica/11.3.0
        Mathematica/12.0.0
        Mathematica/13.1.0
        Mathematica/14.1.0
```

`module spider <name>/<version>` shows how to load one version, including any modules it
needs first.

## Load a specific module

Use `module load` with the full name to get a predictable version:

```
[jose@login1 ~]$ module load IPython/8.14.0-GCCcore-12.3.0
```

Lmod also loads the modules it depends on.

## Check loaded modules

`module list`, or its shorthand `ml`, shows the currently loaded modules, including the
dependencies Lmod loaded for you.

## Save the current session

You can save your loaded modules as a named collection, so that you can easily recreate the
environment later. Choose a descriptive name:

```
[jose@login1 ~]$ module save my-ipython
Saved current collection of modules to: "my-ipython"
```

Collections are stored in `~/.config/lmod`.

## Restore a saved session

Use `module restore` to load a saved collection:

```
[jose@login1 ~]$ module restore my-ipython
Restoring modules from user's my-ipython
```

## Unload all modules

Run `module purge` to unload all currently loaded modules. With a clean environment, load only
the modules you need for your current task.

## Clear the module cache

Lmod keeps a cache of the module trees in `~/.cache/lmod` to make `module avail` and
`module spider` faster. If a module that was just installed doesn't show up, or Lmod reports
modules that no longer exist, delete the cache. Lmod rebuilds it the next time you use it:

```
rm -rf ~/.cache/lmod
```

## Further reading

* [Jeff Layton: Environment Modules – A Great Tool for Clusters](https://www.admin-magazine.com/HPC/Articles/Environment-Modules) (Admin magazine)
* [Lmod: A New Environment Module System](https://lmod.readthedocs.io/en/latest/) (Project documentation)
* [Using installed software (Lmod modules)](https://docs.support.arc.umich.edu/modules/) (Advanced research computing, University of Michigan)
