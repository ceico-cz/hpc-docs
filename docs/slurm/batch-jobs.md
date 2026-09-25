---
title: "Submit a batch job"
wikijs_updated: 2023-11-16
description: "How to submit non-interactive batch job to cluster scheduler."
---

# Submit a batch job

A batch job runs a script on compute nodes without you being logged in to them. This page
walks through a first job on Phoebe; the same steps work on Koios.

## Example code to run

In this tutorial, we will submit a dummy job executing the well-known command `sleep 600`. This command simply pauses for 600 seconds before completing. Once you are acquainted with the job submission process, feel free to replace this placeholder command with the actual command for your application.

## Create the job script

The job script is a file typically containing properties, required resources, and instructions for launching your application/command. Below is an example job script that you can tailor to meet your specific requirements.

```shell
#!/bin/bash
#SBATCH --job-name=sleep2      # a name for the job
#SBATCH --time=00:33:33        # time limit for the whole job
#SBATCH --partition=cpu        # partition to run in
#SBATCH --ntasks=1             # number of (MPI) processes
#SBATCH --cpus-per-task=1      # number of CPUs for each process

echo "sbatch-INFO: start of job"
echo "sbatch-INFO: nodes: ${SLURM_JOB_NODELIST}"
echo "sbatch-INFO: system: ${SLURM_CLUSTER_NAME}"

sleep 600

echo "sbatch-INFO: we're done"
date
```

A job script is an ordinary shell script. Lines starting with `#SBATCH` are options for Slurm:
they say what resources the job needs. Slurm reads them when you submit the script, and the
shell ignores them as comments when the script runs.

All options are described in the [`sbatch` manual](https://slurm.schedmd.com/sbatch.html). The
ones used above:

-   `--job-name=sleep2` gives the job a **name**, which helps when you look for it later, for example among failed jobs in the job history. Avoid spaces and special characters.
-   `--time=00:33:33` sets the **deadline / walltime** for the job. Provide a conservative estimate (x2) of your job's requirements. Always set it: without it, the job gets the partition's maximum (18 days on `cpu`) and usually waits longer to start. The format is in `MM:SS`, `HH:MM:SS`, or `D-HH:MM:SS`. For example, `1-13:12:11` represents one day, 13 hours, 12 minutes, and 11 seconds.
-   `--partition=cpu` designates the specific **partition** where your job is scheduled. `cpu` is the default for batch jobs; see the [Phoebe partitions](../systems/phoebe/index.md#slurm-partitions) and [Koios partitions](../systems/koios/index.md#slurm-partitions) for the others, and [GPU jobs](gpu-jobs.md) for the GPU partitions.
-   `--cpus-per-task=1` sets the **number of CPUs** for each process. On Phoebe's CPU nodes a CPU is one hardware thread, and every core has two, so `--cpus-per-task=64` gets 32 cores. Slurm hands out whole cores, so `--cpus-per-task=1` actually gets one core (2 CPUs). Ask for more CPUs only if your program uses them; `sleep` needs just one.
-   With argument `--mem=4G` one can specify **memory requirements** per node, or per allocated CPU with `--mem-per-cpu=2G`. Without either, Phoebe's CPU partitions give 2 GB per CPU and Koios 3 GB per CPU (see [memory per CPU](index.md#memory-per-cpu)). When memory limits are exceeded, the job is killed to protect other jobs.

## Submit the job

[Log in to the cluster front-end node](../getting-started/ssh.md), copy content of example jobscript from above into e.g. file `jobscript.sh` into your home directory and submit it using sbatch command:

```shell
$ sbatch jobscript.sh  
Submitted batch job 10811 
$
```

The job was created with job ID **10811**.

## Monitor job execution

Depending on the resources you asked for and how busy the cluster is, the job starts immediately or waits in the queue.

### `squeue`

Current status of job scheduler queue can be viewed by command `squeue --me`. The `--me` option filters jobs belonging to the currently logged-in user,

```shell
$ squeue --me
            JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON) 
...
            10811       cpu   sleep2     jose  R       0:01      1 n11 
...
$ 
```

If the job has already finished, it is no longer shown by `squeue`; use `sacct` instead
(see [job history and troubleshooting](troubleshooting.md)).

### `scontrol show job`

In the output above we see that our job 10811 is in state “**R**” - Running at compute node n11. To see more details about particular job, we can use command `scontrol show job=NNNNN` where `NNNN` is the job number:

```shell
$ scontrol show job=10811
JobId=10811 JobName=sleep2
  ...
  JobState=COMPLETED Reason=None Dependency=(null)
  ...
  RunTime=00:00:15 TimeLimit=00:34:00 TimeMin=N/A
  ...
  Partition=cpu AllocNode:Sid=slurm1:1561034
  ...
  NodeList=n11
  ...
  Command=/home/jose/projects/handson1/jobscript.sh
  WorkDir=/home/jose/projects/handson1
  StdErr=/home/jose/projects/handson1/slurm-10811.out
  StdIn=/dev/null
  StdOut=/home/jose/projects/handson1/slurm-10811.out
  ...
$
```

The output is shortened here (`...`). It shows that the job has finished (`JobState=COMPLETED`)
and where its output and error messages went (`StdOut`, `StdErr`). By default, both go to one
file in the directory you submitted the job from.

## Watch the output of a running job

To follow the output of a running job, find its `StdOut` file with `scontrol show job=<jobid>`
and watch it with `tail -F`, for example:

```shell
tail -F ~/projects/handson1/slurm-10811.out
```

## Interrupt or cancel a job

Sometimes, things might go wrong. Already running, or queued job can be cancelled by command `scancel` and job id.

```shell
[jose@login1]$ scancel 10811
```

## Next steps

* [Job history and troubleshooting](troubleshooting.md): `sacct`, job states and why a job is still pending
* [GPU jobs](gpu-jobs.md): request A100 GPUs
* [Interactive sessions](interactive.md): try things out on a compute node before writing a job script
