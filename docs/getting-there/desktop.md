---
title: "Using remote desktop on Phoebe"
wikijs_updated: 2023-11-15
---

# Using remote desktop on Phoebe

Open OnDemand (OOD) is a web portal that simplifies access to high-performance computing (HPC) resources. It provides a user-friendly interface for managing files, submitting jobs, and accessing various HPC tools.

Open OnDemand sessions refer to interactive computing sessions initiated through the Open OnDemand web portal. These sessions are typically used for interactive and on-the-fly analysis, providing users with direct access to the high-performance computing (HPC) resources of our clusters. The Open OnDemand sessions are running on compute nodes allocated by the HPC system specifically for interactive use.

In first chapter we describe starting new session, in the second one how to connect to existing session.

<div class="grid cards" markdown>

-   [:link: Phoebe Remote Desktop screencast at YouTube](https://www.youtube.com/watch?v=TYqsTua9f2M) 

</div>


## Start a new session

!!! warning "Important"
    most of Phoebe services are available from Institute networks or VPN only

### Log in to the OnDemand portal

go to [https://ood.phoebe.ceico.cz](https://ood.phoebe.ceico.cz) and login with your Institute “Kerberos” login (your username is typically the word before `@` in your email) and your password is same you're using for webmail access.

![Open OnDemand login page asking for Kerberos username and password](../screenshot_20220905_190242.png)

### Start a new Desktop session

Click on icon “Phoebe CPU Desktop”

![Open OnDemand dashboard with the Phoebe CPU Desktop app pinned](../ood_howto/screenshot_20220905_190751.png)

### Set the Desktop deadline

In following dialog, select Deadline for the new desktop session in hours. (eg. 8) and click on "Launch" button.  
This will submit the Desktop job to scheduler.

![Phoebe CPU Desktop launch form with partition and number of hours](../ood_howto/screenshot_20220905_191135.png)

### Submit the Desktop session to the scheduler

After submitting job, we can see Desktop job as "**Queued**" with light blue header.

![Desktop session card in the Queued state](../ood_howto/screenshot_20220905_192347.png)

### Access the newly started session

Once scheduler finds proper resources for your Desktop, header of job greens, and blue button "Lauch..." appears.

![Desktop session card in the Running state with compression and image quality sliders](../ood_howto/screenshot_20220905_192559.png)

I recommend to set both Compression and Image Quality to "9" (the highest) and click on "Launch..." button.  
In new tab of browser should be opened remote desktop at Phoebe cluster.

![Remote Xfce desktop running on a Phoebe compute node](../ood_howto/screenshot_20220905_192859.png)

## Reconnect to a running session

As described above, login to the OnDemand portal at [https://ood.phoebe.ceico.cz](https://ood.phoebe.ceico.cz) with your Kerberos username/password. Then, depending on your display resolution, in the top-menu, you should see either "My Interactive Sessions" menu item, or only corresponsing icon. Click on it..



=== "view on narrower screen"


    ![My Interactive Sessions icon in the top menu on a narrow screen](../ood_howto/screenshot_20220905_194245.png)

=== "view on wide screen"


    ![My Interactive Sessions menu item on a wide screen](../ood_howto/screenshot_20220905_194204.png)

..click on "Launch Phoebe CPU Desktop" and your session will be reopened in new tab of browser.

![Running desktop session with the Launch Phoebe CPU Desktop button](../ood_howto/screenshot_20220905_194650.png)

## End a running session

Every running session is consuming part of cluster resources. So after finishing your work, in "My Interactive Sessions" click on red "Delete" button.
