---
title: "CUDA system admin notes"
wikijs_updated: 2024-01-29
tags:
  - "admin"
  - "cuda"
---

# CUDA system admin notes

good source of deep learning stack compatibility is this matrix:

https://docs.nvidia.com/deeplearning/frameworks/support-matrix/index.html

so here is table for desired system state expected to work by vendor engineers:

| Container release | NVIDIA Driver | CUDA|   |   |
|---|---|---|---|---|
| 23.12 | 545 or later | 12.3.2 |   |   |
|   |   |   |   |   |
|   |   |   |   |   |

## Procedure

According to: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Rocky&target_version=8&target_type=rpm_local

### Install the CUDA toolkit

```
wget https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda-repo-rhel8-12-3-local-12.3.2_545.23.08-1.x86_64.rpm
rpm -i cuda-repo-rhel8-12-3-local-12.3.2_545.23.08-1.x86_64.rpm
dnf -y install cuda-toolkit-12-3
```

### Install the NVIDIA driver


If there is already some installed, then:

(545 is number from compatibility matrix above)

```
dnf -y module reset nvidia-driver
dnf -y module install nvidia-driver:545-dkms
```

..and reboot to load driver.

### Create a conda image with TensorFlow

```
conda create --name tf_20240129 python=3.10
conda activate tf_20240129
python -m pip install --upgrade pip
python -m pip install tensorflow
python -m pip install matplotlib jupyterlab
```
