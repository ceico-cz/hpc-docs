---
title: "Phoebe: MIG trial on gpu2 and GPU node topology"
date: 2026-05-06
slug: mig-trial-gpu2
---

# Phoebe: MIG trial on gpu2 and GPU node topology

On 6 May 2026 two of gpu2's eight A100s were split into small MIG instances. The trial was
rolled back on 13–14 May. The CPU topology changes made at the same time stayed.

<!-- more -->

## CPU topology of the GPU nodes

Several attempts on 6 May changed how Slurm sees the CPUs of `gpu1` and `gpu2`:

1. `GetEnvTimeout=2` removed, and `Parameters=l3cache_as_socket` tried on `gpu2`.
2. Replaced by the cluster-wide `SlurmdParameters=numa_node_as_socket`.
3. `gpu1` and `gpu2` redefined from `Sockets=2 CoresPerSocket=32` to
   `Sockets=8 CoresPerSocket=8`: each NUMA node is now a socket.

With 8 "sockets" of 8 cores, each GPU can be bound to the cores closest to it.

## MIG on gpu2

MIG was set up for one specific job that needed small GPU slices, and removed again once the
test was over. It was never meant as a permanent configuration.

`gpu2` was changed from `Gres=gpu:a100:8` to `Gres=gpu:a100:6,gpu:nvidia_a100_1g.10gb:14`:

* `/dev/nvidia0`–`3` and `/dev/nvidia6`–`7` stayed as full A100s.
* `/dev/nvidia4` and `/dev/nvidia5` were each split into seven `1g.10gb` MIG instances (14 in
  total).
* `gres.conf` listed every device by hand (`AutoDetect=off`), with the cores closest to each
  GPU.

On 13–14 May gpu2 went back to `Gres=gpu:a100:8`, with the original one-line `gres.conf`
entry. MIG is disabled on all eight cards today.

## How it was set up

Nothing was scripted and no systemd unit recreates the instances at boot, so MIG did not
survive a reboot. The steps below come from root's shell history on gpu2 and from
`/etc/slurm` on slurm1.

!!! warning "Two GPU numberings"
    `nvidia-smi -i N` uses the PCI bus order. `/dev/nvidiaN` in `gres.conf` uses the device
    minor number. They differ on gpu2 and the minor numbers change between reboots: in May the
    MIG cards were `nvidia-smi -i 6` and `-i 7` (= `/dev/nvidia4` and `/dev/nvidia5`); today
    `-i 6` is `/dev/nvidia0`. Look up the current mapping before changing anything:

    ```bash
    nvidia-smi -q | grep -E '^GPU |Minor Number'
    ```

1. Drain the node and make sure nothing uses the two cards:

    ```bash
    scontrol update node=gpu2 state=drain reason="mig"
    fuser -v /dev/nvidia4 /dev/nvidia5
    ```

2. Enable MIG mode on the two cards (by `nvidia-smi` index). If the card is busy it needs
   `systemctl stop nvidia-persistenced` and `nvidia-smi --gpu-reset -i N`, or a reboot.

    ```bash
    nvidia-smi -i 6 -mig 1
    nvidia-smi -i 7 -mig 1
    ```

3. Create seven `1g.10gb` GPU instances (profile 19, see `nvidia-smi mig -lgip`) on each
   card, each with its compute instance (`-C`):

    ```bash
    nvidia-smi mig -i 6 -cgi 19,19,19,19,19,19,19 -C
    nvidia-smi mig -i 7 -cgi 19,19,19,19,19,19,19 -C
    ```

4. On slurm1, change the `gpu2` node line in `slurm.conf` to
   `Gres=gpu:a100:6,gpu:nvidia_a100_1g.10gb:14` and list every device in `gres.conf`. Each
   MIG instance is the parent `/dev/nvidiaN` plus its two capability files; their numbers are
   in `/proc/driver/nvidia-caps/mig-minors` on gpu2 (`gpu4/gi7/access 606`,
   `gpu4/gi7/ci0/access 607`, ...):

    ```text
    NodeName=gpu2 AutoDetect=off Name=gpu Type=a100 File=/dev/nvidia[0-1] Cores=8-15
    NodeName=gpu2 AutoDetect=off Name=gpu Type=a100 File=/dev/nvidia[2-3] Cores=24-31
    NodeName=gpu2 AutoDetect=off Name=gpu Type=a100 File=/dev/nvidia[6-7] Cores=56-63
    NodeName=gpu2 AutoDetect=off Name=gpu Type=nvidia_a100_1g.10gb MultipleFiles=/dev/nvidia4,/dev/nvidia-caps/nvidia-cap606,/dev/nvidia-caps/nvidia-cap607 Cores=40-47
    # ... one line per MIG instance, 7 on /dev/nvidia4 and 7 on /dev/nvidia5
    ```

5. Restart `slurmctld` on slurm1 and `slurmd` on gpu2, then resume the node.

The full MIG `gres.conf` is kept on slurm1 as
`/etc/slurm/gres.conf.bak-20260513190911-gpu2-physical` (the matching `slurm.conf` has the same
suffix). It is also in the `/etc/slurm` git history (commits `de315ae` and `5dd77a1`), and the
lines are still in the current `gres.conf` and `slurm.conf`, commented out.

## How it was rolled back

```bash
nvidia-smi -i 7 -mig 0
nvidia-smi -i 6 -mig 0
```

Then the `gpu2` lines in `slurm.conf` and `gres.conf` were restored to `Gres=gpu:a100:8` and
the single `gres.conf` line, and `slurmd` was restarted.
