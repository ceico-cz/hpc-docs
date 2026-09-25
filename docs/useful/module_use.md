---
title: "Lmod software module usage"
---

# Lmod software module usage

Lmod (Lua-based Modules) is a module system used in high-performance computing (HPC) environments to manage environment variables and paths for different software packages and libraries. Here's a general guide on how to use Lmod and the environment modules it generates on an HPC system:

## Search for Available Modules

Use the `module avail` command to see a list of available modules:

```
[jose@login1 ~]$ module avail

------------------------------------------------------------------------- /sw/phoebe/2022a/modules/all -------------------------------------------------------------------------
   CFITSIO/4.2.0-GCCcore-11.3.0                       PyTorch/1.12.1-foss-2022a-CUDA-11.7.0    (D)    foss/2022a
   CUDA/11.7.0                                        ROOT/6.28.04-foss-2022a                  (D)    gnuplot/5.4.4-GCCcore-11.3.0              (D)
   CuPy/12.0.0-foss-2022a                      (D)    SciPy-bundle/2022.05-foss-2022a                 matplotlib/3.5.2-foss-2022a
   Cuba/3.0-GCC-11.3.0                         (D)    TensorFlow/2.11.0-foss-2022a-CUDA-11.7.0 (D)    scikit-learn/1.1.3-foss-2022a             (D)
   HDF5/1.12.2-gompi-2022a                            astropy/5.1.1-foss-2022a                 (D)    torchvision/0.13.1-foss-2022a-CUDA-11.7.0 (D)
   IPython/8.5.0-GCCcore-11.3.0                       emcee/3.1.4-foss-2022a                   (D)    zeus-mcmc/2.5.4-foss-2022a                (D)
   OpenCV/4.6.0-foss-2022a-CUDA-11.7.0-contrib (D)    fastai/2.7.10-foss-2022a-CUDA-11.7.0     (D)

------------------------------------------------------------------------- /sw/phoebe/2021b/modules/all -------------------------------------------------------------------------
...
```

## Load a Specific Module

Use the `module load` command to load a specific module:

```
[jose@login1 ~]$ module load IPython/8.5.0-GCCcore-11.3.0
```

## Check Loaded Modules

Use the `module list`, or its shorthand `ml` to see the currently loaded modules:

```
[jose@login1 ~]$ module list

Currently Loaded Modules:
  1) GCCcore/11.3.0                   (H)   7) Tcl/8.6.12-GCCcore-11.3.0    (H)  13) Python/3.10.4-GCCcore-11.3.0    (H)  19) libxslt/1.1.34-GCCcore-11.3.0
       (H)
  2) zlib/1.2.12-GCCcore-11.3.0       (H)   8) SQLite/3.38.3-GCCcore-11.3.0 (H)  14) OpenPGM/5.2.122-GCCcore-11.3.0  (H)  20) lxml/4.9.1-GCCcore-11.3.0 
          (H)
  3) binutils/2.38-GCCcore-11.3.0     (H)   9) XZ/5.2.5-GCCcore-11.3.0      (H)  15) libsodium/1.0.18-GCCcore-11.3.0 (H)  21) BeautifulSoup/4.10.0-GCCcore-
11.3.0 (H)
  4) bzip2/1.0.8-GCCcore-11.3.0       (H)  10) GMP/6.2.1-GCCcore-11.3.0     (H)  16) util-linux/2.38-GCCcore-11.3.0  (H)  22) IPython/8.5.0-GCCcore-11.3.0
  5) ncurses/6.3-GCCcore-11.3.0       (H)  11) libffi/3.4.2-GCCcore-11.3.0  (H)  17) ZeroMQ/4.3.4-GCCcore-11.3.0     (H)
  6) libreadline/8.1.2-GCCcore-11.3.0 (H)  12) OpenSSL/1.1                  (H)  18) libxml2/2.9.13-GCCcore-11.3.0   (H)

  Where:
   H:  Hidden Module
[jose@login1 ~]$
```

## Use module spider for Information or search

The module spider command provides more detailed information about a module and it's capable to look for particular software:

```
[jose@login1 ~]$ module spider tensorflow

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  TensorFlow:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Description:
      An open-source software library for Machine Intelligence

     Versions:
        TensorFlow/2.7.1-foss-2021b-CUDA-11.4.1
        TensorFlow/2.11.0-foss-2022a-CUDA-11.7.0

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  For detailed information about a specific "TensorFlow" package (including how to load the modules) use the module's full name.
  Note that names that have a trailing (E) are extensions provided by other modules.
  For example:

     $ module spider TensorFlow/2.11.0-foss-2022a-CUDA-11.7.0
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 

[jose@login1 ~]$
```

## Save current session

Our systems allow you to save your loaded modules in a file so that you can easily recreate the environment later.

Use the `module save` command to save the current environment to a file. Choose a descriptive name for the session name.

```
[jose@login1 ~]$ module save josef-ipython
Saved current collection of modules to: "josef-ipython"

[jose@login1 ~]$
```

Sessions are stored in `~/.lmod` directory.

## Restore previously saved session

Use the `module restore` command to load the modules saved session previously.

```
[jose@login1 ~]$ module restore josef-ipython
Restoring modules from user's josef-ipython
[jose@login1 ~]$
```

## Cleaning loaded modules

Run the `module purge` command to unload all currently loaded modules. Now that the module environment is clean, you can load the specific modules you need for your current task.

## References / Further reading

* [Jeff Layton: Environment Modules – A Great Tool for Clusters](https://www.admin-magazine.com/HPC/Articles/Environment-Modules) (Admin magazine)
* [Lmod: A New Environment Module System](https://lmod.readthedocs.io/en/latest/) (Project documentation) 
* [Managing software with Lmod](https://arc.umich.edu/document/managing-software-with-lmod/) (Advanced research computing, University of Michigan)
