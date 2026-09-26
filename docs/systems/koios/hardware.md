---
title: "Koios hardware"
wikijs_updated: 2023-11-10
---

# Koios hardware

## Intel Xeon Gold 6130

The CPU of the Koios compute nodes, two per node.

* 16 cores, or 32 SMT virtual cores
* 14 nm technology
* 2.10 GHz base frequency
* [Vendor page](https://www.intel.com/content/www/us/en/products/sku/120492/intel-xeon-gold-6130-processor-22m-cache-2-10-ghz/specifications.html)

## NVIDIA Tesla P100

The GPUs of the Koios GPU node, four cards (currently dedicated to a project).

* CUDA compute capability 6.0 ([list of CUDA GPUs](https://developer.nvidia.com/cuda/gpus))
* [Vendor datasheet](https://images.nvidia.com/content/tesla/pdf/nvidia-tesla-p100-datasheet.pdf)

## Interconnect

* Mellanox MT4115 ConnectX-4, 1× 100 Gb/s InfiniBand EDR per node
