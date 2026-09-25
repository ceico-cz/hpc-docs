---
title: "How to run Cosmolattice at Phoebe HPC system"
wikijs_updated: 2026-03-16
---

# How to run Cosmolattice at Phoebe HPC system

## CosmoLattice on Phoebe

This page describes a currently working way to run CosmoLattice on the Phoebe
cluster.

### Example paths

- Submit directory:
  `/home/your-user/projects/cosmolattice-run`
- Example binary:
  `/home/your-user/projects/cosmolattice/build/dws`

### Important module detail

On Phoebe, the `2022a` toolchain works reliably only if `OpenSSL/1.1` is loaded
explicitly before the other modules.

Use this sequence:

```bash
module purge
module load OpenSSL/1.1
module load CMake/3.23.1-GCCcore-11.3.0
module load HDF5/1.12.2-gompi-2022a
module load foss/2022a
```

### Example build

This example reflects a Phoebe build configuration that has been proven to
work:

```bash
ssh your-user@phoebe.fzu.cz

cd /home/your-user/projects/cosmolattice
mkdir -p build
cd build

module purge
module load OpenSSL/1.1
module load CMake/3.23.1-GCCcore-11.3.0
module load HDF5/1.12.2-gompi-2022a
module load foss/2022a

cmake .. -DMPI=ON -DHDF5=ON -DPFFT=OFF -DMODEL=dws
cmake --build . -j 8
```

The specific working choices here are:

- `MODEL=dws`
- `MPI=ON`
- `HDF5=ON`
- `PFFT=OFF`

If your upstream CosmoLattice checkout targets a different model or optional
feature set, adjust those CMake flags accordingly.


### Typical submission

```bash
ssh jose@phoebe.fzu.cz '
  cd /home/your-user/projects/cosmolattice-run &&
  sbatch --comment="example run" sbatch.sh example.in
'
```

### Output directories

The live Phoebe wrapper creates output directories prefixed by the Slurm job ID:

```text
<SLURM_JOB_ID>_<input-base>
```

That means repeated submissions of the same `.in` file do not collide.

Each run also writes `REPRODUCE.md` into the output directory, including:

- batch script arguments
- Slurm job comment
- effective Slurm job settings
- `scontrol show job` output
- the exact `sbatch.sh` content used for that run

### Buffered vs unbuffered

The current wrapper supports `SLURM_UNBUFFEREDIO` through the submit
environment.

Buffered example:

```bash
ssh jose@phoebe.fzu.cz '
  cd /home/your-user/projects/cosmolattice-run &&
  sbatch --time=00:30:00 --comment="buf_ht128" --export=ALL,SLURM_UNBUFFEREDIO=0 \
    sbatch.sh example.in
'
```

Unbuffered example:

```bash
ssh jose@phoebe.fzu.cz '
  cd /home/your-user/projects/cosmolattice-run &&
  sbatch --time=00:30:00 --comment="unbuf_ht128" --export=ALL,SLURM_UNBUFFEREDIO=1 \
    sbatch.sh example.in
'
```

### Hyperthreading vs no hyperthreading

Phoebe CPU nodes expose `128` logical CPUs per node. To compare with and without
hyperthreading:

- With hyperthreading: use `--ntasks-per-node=128`
- Without hyperthreading: use `--ntasks-per-node=64 --hint=nomultithread`

Example without hyperthreading:

```bash
ssh jose@phoebe.fzu.cz '
  cd /home/your-user/projects/cosmolattice-run &&
  sbatch --time=00:30:00 --comment="unbuf_ht64" --export=ALL,SLURM_UNBUFFEREDIO=1 \
    --ntasks-per-node=64 --hint=nomultithread \
    sbatch.sh example.in
'
```

### Example Slurm batch job for Phoebe

This is an example job script showing a working Phoebe setup:

```bash
#!/usr/bin/bash

#SBATCH --job-name cosmolattice
#SBATCH --partition cpu
#SBATCH --nodes 8
#SBATCH --ntasks-per-node 128
#SBATCH --time 00:30:00
#SBATCH --exclusive
#SBATCH --mem 500G

export SLURM_UNBUFFEREDIO=1

module purge
module load OpenSSL/1.1
module load CMake/3.23.1-GCCcore-11.3.0
module load HDF5/1.12.2-gompi-2022a
module load foss/2022a

INPUT=example.in
OUTDIR=${SLURM_JOB_ID}_${INPUT%.in}

mkdir -p "$OUTDIR"

srun --mpi=pmix_v3 \
  /home/your-user/projects/cosmolattice/build/dws \
  input=${INPUT} \
  outputfile=${OUTDIR}/ \
  baseSeed=31415926
```

### Notes

- `#SBATCH` directives configure `sbatch`, not `srun`.
- `SLURM_UNBUFFEREDIO=1` is the environment-variable equivalent of
  `srun --unbuffered`.
- If you want a free-form note attached to a run, submit with
  `sbatch --comment="..."`.
- Replace the example paths, input file, and binary location with your own
  upstream CosmoLattice checkout and build.
