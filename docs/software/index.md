---
title: "Software"
description: "How software is provided on the CEICO clusters, and guides for specific applications"
---

# Software

## How software is provided

* **Software modules**: most compilers, libraries and scientific packages are installed
  centrally and loaded with Lmod. See [Software modules (Lmod)](modules.md).
* **Conda**: for Python stacks that are not available as modules, create your own conda
  environment. See [Conda on Phoebe](conda.md).
* **uv**: a fast Python package and project manager, used on top of a Python module. See
  [Python with uv](python-uv.md).
* **Without root**: you can still extract binaries from an RPM package into your home
  directory. See [Unpack an RPM without root](unpack-rpm.md).

Modules come in stacks, one per toolchain generation: `2023a` to `2026a` under `/cvmfs`, and a
`system` stack with CUDA, Miniforge3 and commercial software. See
[where modules come from](modules.md#where-modules-come-from).

## Requesting software

!!! warning "TODO"
    Explain how users ask for new software or a new version (contact, ticket system or
    e-mail), and what information to include.

## Application guides

* [CosmoLattice](cosmolattice.md) - lattice simulations of scalar and gauge fields, with MPI
* [CosmoSIS (Python 2.7)](cosmosis-py27.md) - building the Python 2.7 release in conda
* [CuPy on GPUs](cupy.md) - NumPy and SciPy on NVIDIA GPUs
* [MESA stellar evolution](mesa.md) - building and running MESA star with the MESA SDK
* [Pyoperon](pyoperon.md) - symbolic regression, with an optional MPI setup
* [Wolfram Mathematica](mathematica/index.md) - interactive and batch use, licences
