Globus Endpoint Deployment
==========================

This Ansible role performs a deployment of Globus Connect Server 4. The setup
is configured to use MyProxy OAuth for authentication and the accompanying OAuth
page has been customised with a MASSIVE logo and text. These could easily be
adjusted for you own site.

This role installs Globus MyProxy, MyProxyOAuth and Globus GridFTP
(the endpoint) all on the same machine.

Let's Encrypt's CertBot is used to obtain SSL certificates for Apache.

The role was developed using these instructions: https://docs.globus.org/globus-connect-server/v4/#introduction
For information on using Ansible: https://docs.ansible.com/ansible/latest/index.html

Requirements
------------

The role has been tested on CentOS 7.8.

The following firewall ports should be configured as they are not covered by
this role.

-  Port 2811 inbound from 54.237.254.192/29
-  Port 50000 - 51000 inbound/outbound to/from Any.
-  Port 443 outbound to 54.237.254.192/29 and nexus.api.globusonline.org
-  Port 443 outbound to downloads.globus.org
-  Port 443 outbound to crl.cilogon.org
-  Port 7512 inbound from 54.237.254.192/29
-  Port 443 inbound from Any

A DNS entry is required before installing this role.

An account on https://globus.org is required for installation. This could be a Globus ID account, or any of the other supported authentication methods. e.g. Google, ORCiD iD

Example Inventory and Playbook
------------------------------

This repository contains a sample Ansible inventory and playbook.

The inventory file `globusinventory` is setup to create 2 endpoints.

 - 'globus.example.edu.au' On this machine the main globus endpoint is configured with MyProxy OAuth for authentication. As configured in this example an endpoint known as 'globus_username#example' is created.
 - 'globusresearchnetwork' has been created to support a different network interface. This endpoint relies on 'globus.example.edu.au' for authentication. e.g. you have a collection of big data producing instruments on a private network. You wish to use Globus to push data on a high speed private network to the same storage infrastructure as connected to 'globus.example.edu.au'. As configured in this example an endpoint known as 'globus_username#researchnetwork' is created.

> NOTE: In m3_globus/tasks/main.yml a python script 'm3_globus/files/mellanox_ip_address.py' is used to calculate the IP for the DataInterface used in building the 'reseachnetwork' endpoint. This logic will need to be altered to reflect how infrastructure is deployed at your site.

To run the playbook to build both Globus endpoints:

> ansible-playbook  -i globusinventory -l GlobusNodes -t m3_globus globusnodes.yml --ask-vault-pass

You will be prompted to enter the password for ansible-vault.
This will allow Ansible to decrypt the 'globus_password' during installation.

To run the playbook to just build the globus.example.edu.au endpoint:

> ansible-playbook  -i globusinventory -l globus.example.edu.au -t m3_globus globusnodes.yml --ask-vault-pass

Role Variables
--------------

The following variables should be set prior to running the role.

- vars/certbot.yml - Let's Encrypt Certbot configuration
  - certbot_email: contact email address for Let's Encrypt

- vars/globus-auth.yml - Globus account login
  - globus_username: username
  - globus_password: password

> NOTE: the variable ```globus_password``` should be encrypted using
> ```ansible-vault``` when setting up this role. This will ensure that the
> password is not accidentally shared.
>
> To encrypt your globus password: ```ansible-vault encrypt_string yourPasswordGoesHere```
>
> When prompted enter the password to encrypt the string.
> The output is the encrypted Globus password.
> Copy this into globus-auth.yml
>
> It should look like this.
>
```
globus_password: !vault |
                 $ANSIBLE_VAULT;1.1;AES256
                 66386449653236336462626566653063336164663966303231363934653561363064363833313662
                 6643162536303530376336343832656537303632313433360a626438346336353331386135323734
                 62656361653630373231613662633962316233633936396165386439616533353965373339616234
                 3430613539666330390a313736323265656432366236633330313963326365653937323833366536
                 34623731376664623134383463316265643436343438623266623965636363326136
```
> When running the playbook, use the option ```--ask-vault-pass```. This will
> prompt Ansible to ask for the password to decrypt your Globus password.

- vars/globus-connect-server.yml
  - endpoint_Public: (True or False) Should the endpoint be publicly visible ?
  - security_IdentityMethod: OAuth (leave as is but could be 'MyProxy')
  - gridftp_Server: Domain name for the machine where Globus will be installed.
  - gridftp_ServerBehindNAT: True
  - gridftp_RestrictPaths: RW~,RW/scratch,RW/projects,RW/fs03
  - gridftp_RequireEncryption: (True or False) Depending on the sensitivity of your data encryption might be required.  
  - myproxy_Server: Should be the same domain name.
  - myproxy_ServerBehindNAT: True
  - oauth_Server: Should be the same domain name.
  - oauth_ServerBehindNAT: True
  - sharing_enable: (True or False) Sharing can only be used if you are a Globus subscriber
  - sharing_RestrictPaths: R/ (e.g. readonly for the whole filesystem)
  - sharing_StateDir: $HOME/.globus/sharing (The directory Globus uses to manage sharing states for a user)
  - sharing_UsersAllow: "Comma separated list of users"
  - sharing_GroupsAllow: "Comma separated list of groups"
  - sharing_UsersDeny: "Comma separated list of users"
  - sharing_GroupsDeny: "Comma separated list of groups"  

  Note: To use Sharing, your Globus Endpoint needs to be 'managed' under a Globus subscription. Please refer to the Globus Connect Server installation notes on 'Sharing' for a full explanation.

These files will need customising for your site:
- m3_globus/files/authorize.html (update for your site)
- m3_globus/files/massive_logo.png (replace with your logo)
- m3_globus/files/oauth.css (update for your site)

Author Information
------------------

Jay van Schyndel - Monash eResearch Centre
