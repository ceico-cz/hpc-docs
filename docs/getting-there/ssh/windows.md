---
title: "Accessing Phoebe using SSH from Windows"
wikijs_updated: 2023-11-15
---

# Accessing Phoebe using SSH from Windows

!!! info "Note"
    Before first login, initial [activating Phoebe account](../getting-a-user-account.md) is necessary.


## Install an SSH client

We recommend to use Mobatec ssh client, which is available to download [here](https://mobaxterm.mobatek.net/download.html). 

MobaXterm is a popular terminal software that includes an embedded X server and various network tools, including an SSH client. 

## Create a key pair in MobaXterm

### Open MobaXterm

- Launch MobaXterm on your computer.

### Open the MobaKeyGen utility

- In the MobaXterm main window, click on the "Tools" button
- select MobaKeyGen utility

### Configure key generation
  
- Choose the key type (EdDSA provides decent security)

### Consider encrypting the private key

- Type-in `Key passphrase` protecting newly generated key from potential misuse.

### Generate the key pair

- Click the "Generate" button to create the key pair. Move the mouse around in the blank area to generate randomness.

### Save the key pair

- Once the key pair is generated, you can save it to your local machine.
- Click on the "Save private key" button to save the private key. This private key file will typically have a `.ppk` (Putty private key) extension. Select the directory and clisk on `Save` button.
- Click on the "Save public key" button to save the public key. This is the key you'll share with servers or services.
- Copy out Public key from field `Public key for pasting into OpenSSH server` and provide it to Phoebe admin

### Close MobaKeyGen

- Close the MobaKeyGen window once you have saved your keys.

### MobaKeyGen screenshot

![MobaXterm SSH key generator with an Ed25519 key](../../screenshots/screenshot_20231115_171211.png)

## Configure a Phoebe profile in the MobaXterm terminal

1. click on <kbd>Session</kbd> and then <kbd>SSH</kbd>
1. fill-in remote host as `phoebe.fzu.cz`
1. tick the <kbd>Specify username</kbd> checkbox and fill in your koios username ( usually your short FZU username )
1. click on "Advanced SSH settings"
1. tick <kbd>Use private key</kbd> and select the private part of your key
1. click on <kbd>OK</kbd>

## Connect to Phoebe using the profile

In the left column, click on profile created in previous step. Console window should appear.
