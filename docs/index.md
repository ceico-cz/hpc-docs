---
title: "Phoebe compute system wiki"
---

# Phoebe compute system wiki

Phoebe is our current CEICO dept. HPC cluster.

!!! info ""
    In Greek mythology, Phoebe ( *ˈfiːbi* ), sister of Κοῖος was one of the first generation of Titans, who were one set of sons and daughters of Uranus and Gaia.[^wiki_Phoebe]

Phoebe consists from 20 compute nodes, each equipped with 64 powerful CPU cores ( 2xAMD EPYC 7543 [^amd_7543] ), 512 GB of RAM memory and 1.7 TB of blazingly fast NVME[^wiki_NVME] local disk. Additional two *"fat"* GPU nodes are accelerated by 8 GPU NVIDIA A100 [^nvidia_A100] cards, and configured with increased amount 2TB RAM and 3.4 TB of local NVME storage per each node.

Software, user and project data are saved at 218 terabytes of hybrid storage, consisting from both solid and rotational hard drives.

All components of the HPC system are connected together using low-latency 100Gbit Infiniband interconnect fabric.

![gj6uq8gm.jpeg](phoebe_pictures/gj6uq8gm.jpeg)

## Quick start

<div class="grid cards" markdown>

-   [:arrow_right: Run code using CLI (via SSH)](getting-there/ssh.md)
-   [:arrow_right: Run my code in Jupyter Lab (python)](getting-there/using-jupyterLab-at-ondemand.md)
-   [:arrow_right: Run (eg.) Wolfram Mathematica using remote desktop session](getting-there/desktop.md)

</div>

## About the system

| pcs | hostnames | resource | n~cores~ | f~cpu~ (base) | f~cpu~ (max) | RAM | local storage | additional notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20  | `n[1-20]` | cpu compute nodes | 64  | 2.8 GHz | 3.7 GHz | 512 GB | 1.7 TB |  -   |
| 2   | `gpu[1-2]` | gpu-accelerated *fat* nodes | 64  | 2.8 GHz | 3.7 GHz | 2 TB | 3.4 TB | 8x NVIDIA A100 |
| 1   | `phoebe.fzu.cz` | login front-end node | 48  | 3.5 GHz | 4.0 GHz | 368 GB | -  |  -   |

*..in total 1344 fast CPU cores to your disposal!*

### Pictures from the datacenter 



=== "Phoebe indicators blinking into darkness of serverroom"


    ![Phoebe_indicators.jpg](phoebe_pictures/phoebe_realistic_001_small.jpg)

=== "Phoebe disk shelves with storage servers bellow"


    ![Phoebe disk shelves with storage servers below](phoebe_pictures/20220526_201547.jpg){ style="width:35%" } 

=== "Compute nodes with power, Ethernet and Infiniband wiring"


    ![20220526_201437.jpg](phoebe_pictures/20220526_201437.jpg){ style="width:35%" }

=== "Front view at compute nodes"


    ![20230308_130306_2.jpg](phoebe_pictures/20230308_130306_2.jpg)

    -----

### References

[^amd_7543]: [AMD EPYC™ 7543, vendor product page](https://www.amd.com/en/products/cpu/amd-epyc-7543)
[^wiki_NVME]: [Wikipedia: NVME](https://en.wikipedia.org/wiki/NVM_Express)
[^nvidia_A100]: [NVIDIA A100, vendor product page](https://www.nvidia.com/en-us/data-center/a100/)
[^wiki_Phoebe]: [Wikipedia: Phoebe(TItaness) ](https://en.wikipedia.org/wiki/Phoebe_(Titaness))
