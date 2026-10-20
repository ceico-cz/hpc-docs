---
title: "What is an HPC cluster?"
description: "The parts of a high-performance computing cluster, and what they mean for how you work on Phoebe and Koios"
---

# What is an HPC cluster?

An HPC (high-performance computing) cluster is many ordinary servers wired together with a fast
network and shared storage, used as one system. If you have only ever run programs on your
laptop, this page explains the parts of a cluster and why they change how you work. If you
already know clusters, skip ahead to [getting started](index.md).

## Why not just a faster computer?

A single processor core hasn't become much faster in years. Clock speeds stopped at about
4–5 GHz, because a faster chip needs more power and gives off more heat than can be removed
from it. Instead, computers now get more cores, and a cluster takes this further: it puts
hundreds or thousands of cores, and many GPUs, at your disposal by connecting many machines.

The catch is that the extra power comes from **doing many things at the same time**. A program
that uses one core runs no faster on Phoebe than on a good laptop. It pays off when you:

* run a program that uses many cores or GPUs at once (for example with OpenMP, MPI, or a GPU
  library);
* run the same program many times with different inputs, as many independent jobs;
* need more memory, disk space or run time than your own computer has.

## The parts of a cluster

<div class="hpc-diagram">
<svg viewBox="0 0 760 370" role="img" aria-labelledby="hpc-diagram-title" xmlns="http://www.w3.org/2000/svg">
  <title id="hpc-diagram-title">You connect over SSH to the login node; Slurm starts your jobs on the compute nodes; all nodes share storage over the InfiniBand network</title>
  <defs>
    <marker id="hpc-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="arrowhead"/>
    </marker>
  </defs>
  <!-- you -->
  <rect class="box" x="10" y="118" width="120" height="64" rx="6"/>
  <text x="70" y="146" class="label">You</text>
  <text x="70" y="166" class="sub">laptop, browser</text>
  <line class="flow" x1="130" y1="150" x2="186" y2="150" marker-end="url(#hpc-arrow)"/>
  <text x="158" y="140" class="note">SSH</text>
  <!-- login node -->
  <rect class="box accent" x="190" y="118" width="160" height="64" rx="6"/>
  <text x="270" y="146" class="label">Login node</text>
  <text x="270" y="166" class="sub mono">phoebe.fzu.cz</text>
  <!-- scheduler -->
  <rect class="box accent" x="420" y="14" width="190" height="56" rx="6"/>
  <text x="515" y="38" class="label">Scheduler (Slurm)</text>
  <text x="515" y="58" class="sub">queue of waiting jobs</text>
  <path class="flow" d="M300,118 L300,42 L416,42" marker-end="url(#hpc-arrow)"/>
  <text x="308" y="34" class="note start">sbatch, srun</text>
  <line class="flow" x1="515" y1="70" x2="515" y2="104" marker-end="url(#hpc-arrow)"/>
  <text x="523" y="92" class="note start">starts jobs</text>
  <!-- compute nodes -->
  <rect class="group" x="390" y="108" width="360" height="132" rx="8"/>
  <text x="570" y="228" class="sub">compute nodes</text>
  <rect class="box" x="402" y="120" width="76" height="40" rx="4"/><text x="440" y="145" class="sub mono">n1</text>
  <rect class="box" x="488" y="120" width="76" height="40" rx="4"/><text x="526" y="145" class="sub mono">n2</text>
  <rect class="box" x="574" y="120" width="76" height="40" rx="4"/><text x="612" y="145" class="sub mono">…</text>
  <rect class="box" x="660" y="120" width="76" height="40" rx="4"/><text x="698" y="145" class="sub mono">n20</text>
  <rect class="box" x="402" y="168" width="76" height="40" rx="4"/><text x="440" y="193" class="sub mono">gpu1</text>
  <rect class="box" x="488" y="168" width="76" height="40" rx="4"/><text x="526" y="193" class="sub mono">gpu2</text>
  <rect class="box" x="574" y="168" width="76" height="40" rx="4"/><text x="612" y="193" class="sub mono">s1</text>
  <rect class="box" x="660" y="168" width="76" height="40" rx="4"/><text x="698" y="193" class="sub mono">…</text>
  <!-- network -->
  <rect class="net" x="190" y="266" width="560" height="22" rx="11"/>
  <text x="470" y="282" class="net-label">InfiniBand network, 100 Gb/s</text>
  <line class="link" x1="270" y1="182" x2="270" y2="266"/>
  <line class="link" x1="570" y1="240" x2="570" y2="266"/>
  <line class="link" x1="270" y1="288" x2="270" y2="306"/>
  <!-- storage -->
  <path class="box" d="M200,312 a70,10 0 0,0 140,0 v36 a70,10 0 0,1 -140,0 z"/>
  <ellipse class="box" cx="270" cy="312" rx="70" ry="10"/>
  <text x="270" y="342" class="label">Shared storage</text>
  <text x="360" y="336" class="sub start">home, project space and software, the same on every node</text>
</svg>
</div>
/// caption
The parts of a cluster, with the names they have on Phoebe. Koios has the same layout, with
the login node `koios1.fzu.cz`.
///

**Login node**
:   The machine you connect to with [SSH](ssh.md), `phoebe.fzu.cz` on Phoebe and `koios1.fzu.cz`
    on Koios. Here you edit files, compile code, manage your data and submit jobs. Everyone
    shares it, so **don't run heavy computations on the login node**: they slow it down for all
    users.

**Compute nodes**
:   The machines that do the work. Phoebe has 20 CPU nodes with 64 cores each, two GPU nodes
    with 8 NVIDIA A100 cards each, and three small nodes for light interactive work. You don't
    log in to them directly; the scheduler gives you a share of them. See the
    [Phoebe](../systems/phoebe/index.md) and [Koios](../systems/koios/index.md) pages for details.

**Scheduler**
:   [Slurm](../compute/index.md) keeps a queue of jobs. You tell it what your job needs (cores,
    memory, GPUs, run time), and it starts the job on compute nodes as soon as those resources
    are free. Until then the job waits in the queue. Groups of nodes with their own limits are
    called *partitions*.

**Network**
:   A fast, low-latency InfiniBand network connects all nodes. Programs that run on several
    nodes at once, such as MPI codes, exchange data over it, and it carries all traffic to the
    shared storage.

**Shared storage**
:   Your home directory, the project space and the software tree are on network storage that
    every node sees. A file you create on the login node is there, at the same path, when your
    job runs on a compute node. See [storage and software](../systems/storage.md).

## What this means for you

* **You work in jobs.** You describe the work in a [batch job](../compute/batch-jobs.md) script
  and submit it, or ask for an [interactive session](../compute/interactive.md) on a compute
  node. Your job may wait before it starts, and it is stopped when it reaches its time limit.
* **Ask for what you use.** A job that asks for 64 cores but uses one keeps the other 63 from
  everyone else, and larger requests usually wait longer in the queue.
* **Your program has to run in parallel** to profit from many cores, or you split the work into
  many independent jobs.
* **You set up your own software environment.** Load what is installed with
  [modules](../software/modules.md), or install packages into your home directory with
  [conda](../software/conda.md), [uv](../software/python-uv.md) or a
  [container](../software/apptainer.md). You have no administrator rights.
* **Data isn't backed up.** Keep copies of important files elsewhere.

Ready to start? Continue with [getting started](index.md).
