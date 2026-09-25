---
title: "Phoebe hardware"
wikijs_updated: 2024-01-22
description: "Phoebe supercomputer consists from many components..."
---

# Phoebe hardware

Phoebe supercomputer is placed in datacenter of Institute of Physics and infrastructure is managed with cooperation with [Computing centre (CC) of FZU.](https://www.farm.particle.cz/en/o-nas/).


## Compute nodes (20×, n[1-20])

* Server/platform: Gigabyte H262-Z63 / Motherboard: MZ62-HD0-00 ([vendor link](https://www.gigabyte.com/Enterprise/High-Density-Server/H262-Z63-rev-100))
* CPU: 64 cores - 2x AMD EPYC 7543 ([vendor link](https://www.amd.com/en/products/cpu/amd-epyc-7543))
* Memory: 512 GB - 16ks 32GB Samsung DDR4 3200 MHz ECC M393A4K40EB3-CWE
* 100Gbit HPC interconnect adapter: single port Mellanox/Nvidia ConnectX 6 MT28908 Infiniband PCI-E card
* Ethernet adapter: dual-port 10Gbit Broadcom BCM57416 PCI-E card
* 1,92TB NVMe KINGSTON SEDC1500M1920G
* p~max~ = 360W / node

![compute_node_block_diagram.png](phoebe_hw_diagrams/compute_node_block_diagram.png)

## GPU-accelerated compute nodes (2×, gpu[1-2])

* Server/platform: HPE ProLiant XL675d Gen10 Plus
* CPU: 64 cores - 2x AMD EPYC 7543 ([vendor link](https://www.amd.com/en/products/cpu/amd-epyc-7543))
* GPU: 8x NVIDIA A100-SXM with 80GB RAM connected with nvlink interconnect
* Memory: 2TB - 32ks 64GB SK Hynix DDR4 2933 MHz ECC HMAA8GR7AJR4N-XN
* 100Gbit HPC interconnect adapter: single port Mellanox/Nvidia ConnectX 6 MT28908 Infiniband PCI-E card
* Ethernet adapter: dual-port 10Gbit Marvell FastLinQ 41000 Series 
* 3.8TB NVMe HPE MZXL53T8HBLS-000H3
* p~max~ = 3.5 kW / node


## Fast sequential CPU nodes (2×, hv[1-2], a.k.a. ssh:phoebe.fzu.cz)

* Server/platform: Asus RS700A-E11-RS12U
* CPU: 32 cores up to 4GHz - 2x AMD EPYC 73F3 16-Core CPU ([vendor link](https://www.amd.com/en/products/cpu/amd-epyc-73f3))
* Memory: 512GB - 16ks 32GB SK Hynix DDR4  3200 MT/s ECC HMA84GR7DJR4N-XN
* p~max~ = 696 W


## High speed interconnect network

* Infiniband MQM8700 Mellanox Quantum™ HDR Edge Switch ([vendor_link](https://network.nvidia.com/files/doc-2020/pb-qm8700.pdf))
* servers connected with bandwidth of 100Gbit using splitter cables 
* offers 40x200Gbit or 80x100Gbit port configuration, redundant PSU
* p~max~ = 189 W

## Ethernet network equipment

* p~max~ = 132 W

## Storage infrastructure

## Power management
