---
title: "Troubleshooting Slurm jobs"
wikijs_updated: 2023-11-16
---

# Troubleshooting Slurm jobs

## Get the Slurm job state

### `sacct`

`sacct` command is used to read data from accounting database. This particular command will search for jobs of user `jose`, in past month:

```
sacct -u jose --format=jobid,user,jobname%22,partition,state%20,NodeList,Start,End,Elapsed --starttime=$(date --date='-1 month' +%Y-%m-%d)
```

(note the `%` symbol used to enhance correct table formatting - eg. `%22` reserves 22 characters )

#### `sacct` example

In example we see the job `1410269` was `CANCELLED`:

```
$ sacct
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode 
------------ ---------- ---------- ---------- ---------- ---------- -------- 
1410269      sys/dashb+    cpu_int   fzu_a_39         16 CANCELLED+      0:0 
1410269.bat+      batch              fzu_a_39         16  CANCELLED     0:15 
1410269.ext+     extern              fzu_a_39         16  COMPLETED      0:0 
$ 
```

### Understanding the job state

Possible job states are:

* `FAILED`: Typically caused by application errors, such as the program ending with a non-zero return code, a segmentation fault, etc.

* `OUT_OF_MEMORY`: This occurs when the application attempts to allocate more memory than the reserved amount. It's important to note that the default memory allocation per job is proportional to the number of reserved CPUs. If your software has higher memory requirements, consider specifying the `--mem` argument in the sbatch script to request an appropriate amount of memory.

* `COMPLETED`: Indicates that the job ended successfully, returning a zero return code.

* `CANCELLED` by 30012: This status occurs when a user with UID 30012 cancels the job.

* `PENDING`: Indicates that the job is waiting for available resources in the queue.

## Get the Slurm job stdout and stderr

`stdout` and `stderr` can provide valuable diagnostic information when debugging. 

!!! info "Note"
    `stdout` stands for standard output, and it is one of the three standard data streams in a computer, along with standard input (`stdin`) and standard error (`stderr`). These streams are fundamental communication channels between a program and its environment.
