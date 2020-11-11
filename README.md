Globus Endpoint Deployment
==========================

This role performs a deployment of Globus Connect Server 4. The setup
is configured to use MyProxy OAuth for authentication and the accompanying OAuth
page has been customised with a MASSIVE logo and text. These could easily be
adjusted for you own site.

This role installs Globus MyProxy, MyProxyOAuth and Globus GridFTP
(the endpoint) all on the same machine.

Let's Encrypt's CertBot is used to obtain SSL certificates for Apache.

The role was developed using these instructions: https://docs.globus.org/globus-connect-server/v4/#introduction

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
