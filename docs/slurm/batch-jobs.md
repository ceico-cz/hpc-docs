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
#SBATCH --job-name=NameOfJob   # specify job name
#SBATCH --time=00:33:33        # set a limit on the total run time
#SBATCH --partition=cpu        # specify partition name
#SBATCH --ntasks=1             # specify number of (MPI) processes
#SBATCH --cpus-per-task=64     # specify amount of cpu cores per task

echo "sbatch-INFO: start of job"
echo "sbatch-INFO: nodes: ${SLURM_JOB_NODELIST}"
echo "sbatch-INFO: system: ${SLURM_CLUSTER_NAME}"

sleep 600

echo "sbatch-INFO: we're done"
date
```

A batch script in SLURM is essentially a standard shell script. Any line in the script that begins with the `#SBATCH` keyword is considered to contain metadata specific to the SLURM job, providing configuration and instructions for job execution.

All options of jobscript are described here: [https://slurm.schedmd.com/sbatch.html](https://slurm.schedmd.com/sbatch.html) - so only quick review of  options used above:
-   `--job-name=NameOfJob` **name** your job with some descriptive name. It can be useful when looking for eg. failed jobs in the history of scheduler. Avoid including spaces or special characters in the job name
-   `--time=00:33:33` sets the **deadline / walltime** for the job. Provide a conservative estimate (x2) of your job's requirements. Always set it: without it, the job gets the partition's maximum (18 days on `cpu`) and usually waits longer to start. The format is in `MM:SS`, `HH:MM:SS`, or `D-HH:MM:SS`. For example, `1-13:12:11` represents one day, 13 hours, 12 minutes, and 11 seconds.
-   `--partition=cpu` designates the specific **partition** where your job is scheduled. `cpu` is the default for batch jobs; see the [Phoebe partitions](../systems/phoebe.md#slurm-partitions) and [Koios partitions](../koios.md) for the others, and [GPU jobs](gpu-jobs.md) for the GPU partitions.
-   `--cpus-per-task=64` determines the **number of CPU cores** allocated to each process. Certain applications can leverage multiple cores, so it is meaningful to allocate an appropriate number of cores to enhance their performance.
-   With argument `--mem=4G` one can specify **memory requirements** per node, or per allocated CPU with `--mem-per-cpu=2G`. Without either, Phoebe's CPU partitions give 2 GB per CPU and Koios 3 GB per CPU (see [memory per CPU](index.md#memory-per-cpu)). When memory limits are exceeded, the job is killed to protect other jobs.

## Submit the job

[Log in to the cluster front-end node](../getting-there/ssh.md), copy content of example jobscript from above into e.g. file `jobscript.sh` into your home directory and submit it using sbatch command:

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
  UserId=jose(30012) GroupId=jose(30012) MCS_label=N/A 
  Priority=50000 Nice=0 Account=fzu_a_39 QOS=normal 
  JobState=COMPLETED Reason=None Dependency=(null) 
  Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0 
  RunTime=00:00:15 TimeLimit=00:34:00 TimeMin=N/A 
  SubmitTime=2022-10-06T13:40:52 EligibleTime=2022-10-06T13:40:52 
  AccrueTime=2022-10-06T13:40:52 
  StartTime=2022-10-06T13:40:52 EndTime=2022-10-06T13:41:07 Deadline=N/A 
  SuspendTime=None SecsPreSuspend=0 LastSchedEval=2022-10-06T13:40:52 Scheduler=Backfill 
  Partition=cpu AllocNode:Sid=slurm1:1561034 
  ReqNodeList=(null) ExcNodeList=(null) 
  NodeList=n11 
  BatchHost=n11 
  NumNodes=1 NumCPUs=64 NumTasks=1 CPUs/Task=64 ReqB:S:C:T=0:0:*:2 
  TRES=cpu=64,node=1,billing=64 
  Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=* 
  MinCPUsNode=64 MinMemoryNode=0 MinTmpDiskNode=0 
  Features=(null) DelayBoot=00:00:00 
  OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null) 
  Command=/home/jose/projects/handson1/jobscript.sh 
  WorkDir=/home/jose/projects/handson1 
  StdErr=/home/jose/projects/handson1/slurm-10811.out 
  StdIn=/dev/null 
  StdOut=/home/jose/projects/handson1/slurm-10811.out 
  Power= 
$
```

From that output we can see our job already finished (`JobState=COMPLETED`) and we see files, where `stderr` and `stdout` were forwarded to. By default, these files are in the job submission directory.

## Watch the output of a running job

To see live output of job, using `scontrol show job=NNNNN` find the `StdOut` file path, and watch it using tail command - eg. 

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
