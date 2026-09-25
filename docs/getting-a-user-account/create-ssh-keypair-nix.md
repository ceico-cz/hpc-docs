---
title: "Create an SSH key pair on Linux / macOS"
wikijs_updated: 2022-09-06
---

# Create an SSH key pair on Linux / macOS

If you do not have an SSH key pair yet, open a terminal and run:

```bash
ssh-keygen -t ed25519
```

`ssh-keygen` then asks two questions:

1. **Enter file in which to save the key** – press <kbd>Enter</kbd> to accept the default location (`~/.ssh/id_ed25519`).
2. **Enter passphrase** – type a [strong passphrase](https://en.wikipedia.org/wiki/Passphrase) and repeat it.
   If your disk is encrypted, you may leave it empty and just press <kbd>Enter</kbd> twice.

??? example "Example output"

    ```text
    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/home/testuser/.ssh/id_ed25519):
    Created directory '/home/testuser/.ssh'.
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/testuser/.ssh/id_ed25519
    Your public key has been saved in /home/testuser/.ssh/id_ed25519.pub
    The key fingerprint is:
    SHA256:SLKcljiOmsdTubEGeG+6QP+nDs0NoLciBA71guz8BXQ testuser@hostname
    The key's randomart image is:
    +--[ED25519 256]--+
    |  .. E           |
    |.o...            |
    |+..oo .          |
    |* .+o* .         |
    | Oo.*+. S        |
    |+o*oO o          |
    |++.O * .         |
    |oo= O  .         |
    |o.o*.+o          |
    +----[SHA256]-----+
    ```

Print your **public** key and send it to the CEICO HPC administrator:

```bash
cat ~/.ssh/id_ed25519.pub
```

!!! warning
    Never share the private key `~/.ssh/id_ed25519` (the file without `.pub`).
