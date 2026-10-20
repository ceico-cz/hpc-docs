---
title: "Containers with Apptainer"
description: "Run Docker and Apptainer container images on Phoebe and Koios, in batch jobs and on GPUs"
---

# Containers with Apptainer

A container image packs a program together with its whole software environment: its Linux
distribution, libraries and Python packages. With Apptainer (formerly Singularity) you can
run such images on the clusters as a normal user, without root. Use it when software is hard
to build from modules, or when its developers ship a Docker image.

Apptainer is installed on the login nodes and compute nodes of both Phoebe and Koios. The
command `singularity` still works as an alias for `apptainer`.

## Shared images on Phoebe

Some large images are ready to use in `/cvmfs/apptainer.phoebe.lan`, so you don't need to
download them yourself:

| Image | Path |
| --- | --- |
| NVIDIA NGC PyTorch | `/cvmfs/apptainer.phoebe.lan/nvcr.io/nvidia/pytorch/latest/` |
| NVIDIA CUDA deep-learning base | `/cvmfs/apptainer.phoebe.lan/nvcr.io/nvidia/cuda-dl-base/latest/` |
| TensorFlow with Jupyter (GPU) | `/cvmfs/apptainer.phoebe.lan/tensorflow_apptainer/` |
| Google Colab runtime (CPU and GPU), see [Google Colab on Phoebe](../compute/colab/index.md) | `/cvmfs/apptainer.phoebe.lan/colab/` |
| Wolfram Engine | `/cvmfs/apptainer.phoebe.lan/wolfram_engine_apptainer/` |

Most directories have a `README.md` that says which image the file was built from. `latest`
points to the newest version; use the versioned directory next to it if your results must be
reproducible. This repository is not available on Koios.

## Get an image from Docker Hub

`apptainer pull` downloads a Docker image and converts it into one `.sif` file:

```
[jose@login1 ~]$ apptainer pull alpine.sif docker://alpine:3.20
[jose@login1 ~]$ apptainer exec alpine.sif cat /etc/alpine-release
3.20.10
```

Images from other registries work the same way, for example
`docker://nvcr.io/nvidia/pytorch:26.05-py3` or `docker://ghcr.io/<owner>/<image>:<tag>`.
Pull images on the login node, then use the `.sif` file in your jobs.

## Run a container

* `apptainer exec <image> <command>` runs one command inside the container.
* `apptainer shell <image>` opens an interactive shell inside it; the prompt changes to
  `Apptainer>`. Type `exit` to leave.
* `apptainer run <image>` runs the image's default command, if it has one.

Inside the container you are the same user as outside. Your home directory, `/tmp` and the
current directory are available, so your files are where you expect them. Other paths must be
bound with `-B`. For example, `/cvmfs` is not visible unless you add `-B /cvmfs`:

```
apptainer exec -B /cvmfs alpine.sif ls /cvmfs/apptainer.phoebe.lan
```

## Use a container in a batch job

Put the `apptainer exec` command in your job script where you would start your program. This
runs the PyTorch image on a CPU node:

```shell
#!/bin/bash
#SBATCH --job-name=container
#SBATCH --time=00:30:00
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4

image=/cvmfs/apptainer.phoebe.lan/nvcr.io/nvidia/pytorch/latest/pytorch_26.05-py3.sif

apptainer exec "$image" python my_script.py
```

See [Submit a batch job](../compute/batch-jobs.md) for the `#SBATCH` options.

## GPUs

Add `--nv` to give the container access to the NVIDIA GPUs of your job. The GPU driver comes
from the node, the CUDA libraries from the image. Request a GPU as described in
[GPU jobs](../compute/gpu-jobs.md):

```
[jose@login1 ~]$ srun --partition=rocky10 --gres=gpu:a100:1 --cpus-per-task=2 --mem=16G --time=00:10:00 \
    apptainer exec --nv /cvmfs/apptainer.phoebe.lan/nvcr.io/nvidia/pytorch/latest/pytorch_26.05-py3.sif \
    python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
True NVIDIA A100-SXM4-80GB
```

The Koios P100 GPUs are not supported by CUDA 13 or newer. On Koios, use an image built with
CUDA 12 or older; current NGC images such as the PyTorch one above need a newer GPU.

## Disk space

Apptainer keeps downloaded image layers in a cache, `~/.apptainer/cache`, so a second pull of
the same image is faster. The cache can grow to tens of gigabytes in your home directory.
Check and clean it with:

```
apptainer cache list
apptainer cache clean
```

Building a large image needs a lot of temporary space. If `apptainer pull` fails with
"no space left on device", point its temporary directory to your home directory and try
again:

```
mkdir -p ~/apptainer-tmp
export APPTAINER_TMPDIR=~/apptainer-tmp
```

## Further reading

* [Apptainer user guide](https://apptainer.org/docs/user/latest/)
* [Apptainer and MPI applications](https://apptainer.org/docs/user/latest/mpi.html)
