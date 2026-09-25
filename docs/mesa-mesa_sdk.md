---
title: "Running MESA star with the MESA SDK"
wikijs_updated: 2023-11-16
---

# Running MESA star with the MESA SDK

This how-to discuss usage of Modules for Experiments in Stellar Astrophysics (MESA), an open-source 1D stellar evolution code at Phoebe cluster.

## Configure the shell environment for the SDK

As the current Mesa SDK is already unpacked in the Phoebe shared filesystem, it is essential to configure the relevant environment variables:

```shell
export MESASDK_ROOT=/sw/phoebe/standalone/bh/mesasdk-22.6.1
source $MESASDK_ROOT/bin/mesasdk_init.sh
```

## Download and unpack MESA star, and configure the environment

Create a suitable directory in your homedir, navigate to it using the 'cd' command, download the Mesa Star zip file, and ununpack it in that directory

```shell
mkdir -p ~/projects/mesaStar
cd ~/projects/mesaStar
wget https://zenodo.org/record/6547951/files/mesa-r22.05.1.zip
unzip ./mesa-r22.05.1.zip
```

There in `~/projects/mesaStar` , we should see unpacked archive:

```shell
[user@login1 mesaStar]$ ll 
total 2048836 
drwxrwxr-x. 34 jose jose         54 11. kvě 21.35 mesa-r22.05.1 
-rw-rw-r--.  1 jose jose 2098006607 27. srp 21.51 mesa-r22.05.1.zip 
[user@login1 mesaStar]$
```

cd into unpacked archive and get current directory with command `pwd`.

```shell
[user@login1 mesaStar]$ cd mesa-r22.05.1/ 
[user@login1 mesa-r22.05.1]$ pwd 
/home/jose/projects/mesaStar/mesa-r22.05.1 
[user@login1 mesa-r22.05.1]$
```

export the path returned by command `pwd` as `MESA_DIR`:

```shell
export MESA_DIR=/home/jose/projects/mesaStar/mesa-r22.05.1
```

## Compile MESA star

cd to `$MESA_DIR` directory and build mesa STAR:

```shell
cd $MESA_DIR
./install
```

Installation script can take some time as it performs checks if code is working properly.

Once the installation is done, message `MESA installation was successful` will be shown.

## Configure MESA SDK and MESA star permanently in `~/.bashrc`

To avoid the need to export again environment variables as it was done above, one can modify own `~/.bashrc` file .

Open own `~/.bashrc` in nano (or in any editor of your choice)

```shell
nano ~/.bashrc
```

and **append** (do not forget to modify the MESA\_DIR to reflect your mesa star installation directory! )

```shell
export MESASDK_ROOT=/sw/phoebe/standalone/bh/mesasdk-22.6.1 
source $MESASDK_ROOT/bin/mesasdk_init.sh 
export MESA_DIR=/home/jose/projects/mesaStar/mesa-r22.05.1
```

in all **new** shells, since now, mesa and mesaSDK will be activated automatically.

## Further reading

-   Installing MESA - [https://docs.mesastar.org/en/release-r22.05.1/installation.html](https://docs.mesastar.org/en/release-r22.05.1/installation.html)
-   Modules for Experiments in Stellar Astrophysics (MESA) - [https://zenodo.org/record/6547951](https://zenodo.org/record/6547951)
-   MESA SDK - [http://user.astro.wisc.edu/~townsend/static.php?ref=mesasdk](http://user.astro.wisc.edu/~townsend/static.php?ref=mesasdk)
