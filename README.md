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

Role Variables
--------------

The following variables should be set prior to running the role.

- vars/host.yml - Used to ensure the hostname of the machine is set correctly.
  - hostname: Your hostname. e.g. globus.example.edu.au

- vars/certbot.yml - Let's Encrypt Certbot configuration
  - certbot_email: contact email address for Let's Encrypt

- vars/globus-auth.yml - Globus account login
  - globus_username: username
  - globus_password: password

> NOTE: the variable ```globus_password``` should be encrypted using
> ```ansible-vault``` when setting up this role. This will ensure that the
> password is not accidentally shared.
>
> To encrypt your globus password: ```ansible-vault encrypt-string yourPasswordGoesHere```
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
  - endpoint_Name: Name for your endpoint. e.g. MASSIVE
  - endpoint_Public: (True or False) Should the endpoint be publicly visible ?
  - security_IdentityMethod: OAuth (leave as is but could be 'MyProxy')
  - gridftp_Server: Should be the same as 'hostname'.
  - gridftp_ServerBehindNAT: True
  - gridftp_DataInterface: Should be the same as 'hostname'.
  - gridftp_RestrictPaths: RW~,RW/scratch,RW/projects,RW/fs03
  - gridftp_RequireEncryption: (True or False) Depending on the sensitivity of your data encryption might be required.  
  - myproxy_Server: Should be the same as 'hostname'.
  - myproxy_ServerBehindNAT: True
  - oauth_Server: Should be the same as 'hostname'.
  - oauth_ServerBehindNAT: True

Example Playbook
----------------

To run the playbook:

> ansible-playbook --verbose globus_role.yml --ask-vault-pass

You will be prompted to enter the password for ansible-vault.
This will allow Ansible to decrypt the 'globus_password' during installation.

```
---
- name: Deploy Globus
  hosts: globus-test
  become: true

  pre_tasks:
    - debug:
        msg: 'Beginning Globus configuration.'

  roles:
    - m3_globus

  post_tasks:
    - debug:
        msg: 'Globus has been configured.'
```

Author Information
------------------

Jay van Schyndel - Monash eResearch Centre
