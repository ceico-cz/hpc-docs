---
title: "Submit batch job"
description: "How to submit non-interactive batch job to cluster scheduler."
---

# Submit batch job

At Phoebe cluster, we use workload manager [slurm](https://slurm.schedmd.com) to schedule user jobs over compute nodes.

## Example “code” to run

In this tutorial, we will submit a dummy job executing the well-known command `sleep 600`. This command simply pauses for 600 seconds before completing. Once you are acquainted with the job submission process, feel free to replace this placeholder command with the actual command for your application.

## Create jobscript

The job script is a file typically containing properties, required resources, and instructions for launching your application/command. Below is an example job script that you can tailor to meet your specific requirements.

```shell
#!/bin/bash
#SBATCH --job-name=NameOfJob   # specify job name
#SBATCH --time=00:33:33        # set a limit on the total run time
#SBATCH --partition=cpu        # specify partition name (cpu/gpu)
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
-   `--time=00:33:33` sets the **deadline / walltime** for the job. Provide a conservative estimate (x2) of your job's requirements to prevent jobs from getting stuck or blocking the cluster for an extended period. The format is in `MM:SS`, `HH:MM:SS`, or `D-HH:MM:SS`. For example, `1-13:12:11` represents one day, 13 hours, 12 minutes, and 11 seconds.
-   `--partition=cpu` designates the specific **partition** where your job is scheduled. Currently, users of the Phoebe cluster have the option to choose between the cpu and gpu partitions.
-   `--cpus-per-task=64` determines the **number of CPU cores** allocated to each process. Certain applications can leverage multiple cores, so it is meaningful to allocate an appropriate number of cores to enhance their performance.
- With argument `--mem=4G` one can specify **memory requirements** in total, or per allocated CPU with `-mem-per-cpu=2G`. Please note, that Koios allocates 3GB/cpu and Phoebe 2GB/cpu. When memory limits are exceeded, the job will be terminated to protect other jobs from memory issues.

## Submit the job

[Login to cluster front-end node](getting-there/ssh.md), copy content of example jobscript from above into e.g. file `jobscript.sh` into your home directory and submit it using sbatch command:

```shell
$ sbatch jobscript.sh  
Submitted batch job 10810 
$
```

Job was apparently successfully created under job id **10810**.

## Monitor job execution

Depending on the lenght/duration of your job, state of queue at cluster the job might be started immediately, or it can wait in the queue to get requested resources.

### squeue command

Current status of job scheduler queue can be viewed by command `squeue --me`. The `--me` option filters jobs belonging to the currently logged-in user,

```shell
$ squeue --me
            JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON) 
...
            10811       cpu   sleep2     jose  R       0:01      1 n11 
...
$ 
```

### sacct command

If job already finished/failed, it's not anymore visible in squeue. Use `sacct` command to see recent jobs:

```shell
$ sacct
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode 
------------ ---------- ---------- ---------- ---------- ---------- -------- 
1410269      sys/dashb+    cpu_int   fzu_a_39         16 CANCELLED+      0:0 
1410269.bat+      batch              fzu_a_39         16  CANCELLED     0:15 
1410269.ext+     extern              fzu_a_39         16  COMPLETED      0:0 
$
```


### scontrol show job command

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

## Watching output of running job

To see live output of job, using `scontrol show job=NNNNN` find the `StdOut` file path, and watch it using tail command - eg. 

```shell
tail -F /home/jose/projects/handson1/slurm-10811.out
```

## Interrupt / cancel a job

Sometimes, things might go wrong. Already running, or queued job can be cancelled by command `scancel` and job id.

```shell
[jose@login1]$ scancel 10811
```

## Searching in history of jobs

`sacct` (**S**lurm  **acc**ounting) command can show important information about job runtime, results, etc. 

For example, command `sacct --format=jobid,User,jobname%22,partition,state,NNodes%5,NodeList,Start,End,Elapsed,UserCPU --starttime=2022-09-30` will show jobs started after 30.9.2022 for currently logged-in user:

```shell
$ sacct --format=jobid,User,jobname%22,partition,state,NNodes%5,NodeList,Start,End,Elapsed,UserCPU --starttime=2022-09-30 
JobID             User                JobName  Partition      State NNode        NodeList               Start                 End    Elapsed    UserCPU  
------------ --------- ---------------------- ---------- ---------- ----- --------------- ------------------- ------------------- ---------- ----------  
1333              jose sys/dashboard/sys/ood+        cpu CANCELLED+     1              n2 2022-09-30T16:03:13 2022-09-30T16:11:13   00:08:00  00:10.340  
1333.batch                              batch             CANCELLED     1              n2 2022-09-30T16:03:13 2022-09-30T16:11:14   00:08:01  00:10.340  
1334              jose sys/dashboard/sys/bc_+        cpu CANCELLED+     1              n1 2022-09-30T16:08:29 2022-09-30T16:11:11   00:02:42  00:13.169  
1334.batch                              batch             CANCELLED     1              n1 2022-09-30T16:08:29 2022-09-30T16:11:12   00:02:43  00:13.169  
8096              jose sys/dashboard/sys/ood+        cpu    RUNNING     1             n11 2022-10-05T18:54:19             Unknown 1-17:10:12   00:00:00  
8096.batch                              batch               RUNNING     1             n11 2022-10-05T18:54:19             Unknown 1-17:10:12   00:00:00  
8106              jose                   echo        cpu  COMPLETED     1             n11 2022-10-05T19:09:50 2022-10-05T19:09:50   00:00:00   00:00:00  
8106.0                                   echo             COMPLETED     1             n11 2022-10-05T19:09:50 2022-10-05T19:09:50   00:00:00   00:00:00  
$
```
