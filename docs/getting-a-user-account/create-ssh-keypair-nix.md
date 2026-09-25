---
title: "Create ssh keypair at Linux / Mac OS"
---

# Create ssh keypair at Linux / Mac OS

At both Linux or Mac machines, if you do not have existing key/pair, run command `ssh-keygen -t ed25519`.

You'll be asked:

<kbd>Enter file in which to save the key (/home/testuser/.ssh/id_ed25519)</kbd> → just press Enter.

<kbd>Enter passphrase (empty for no passphrase)</kbd> : If you do not have hard-drive encryption, use secure enough passphrase[^1] to protect your key. If your laptop is encrypted, you might decide to do not set ssh key encryption, and just press Enter.

[^1]: https://en.wikipedia.org/wiki/Passphrase



Example:
```
testuser@hostname:~$ ssh-keygen -t ed25519
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
testuser@hostname:~$
```
