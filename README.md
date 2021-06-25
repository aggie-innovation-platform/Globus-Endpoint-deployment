Globus Endpoint Deployment
==========================

These Ansible roles perform a deployment of Globus Connect Server 5.4. The
complete installation is split into two separate roles as a manual task is
required. The roles have been written for easy configuration for your site.

The roles install Globus Connect Server v5.4, creating an endpoint,
storage-gateway and collection on the same machine. Please note the terminology
has changed under version 5. For an explanation please refer to:
https://docs.globus.org/globus-connect-server/v5.4/#globus_connect_version_5_terminology

The roles were developed using these instructions: https://docs.globus.org/globus-connect-server/v5.4/
For information on using Ansible: https://docs.ansible.com/ansible/latest/index.html

Requirements
------------

The role has been tested on CentOS 7.8.

The following firewall ports should be configured as they are not covered by
this role.

-  Port 50000 - 51000 outbound to Any.
-  Port 50000 - 51000 inbound from Any.
-  Port 443 outbound to Any
-  Port 443 inbound from Any

Example Inventory and Playbook
------------------------------

This repository contains a sample Ansible inventory and playbook.

The inventory file `globusinventory` is setup to cater for three different configurations.
- Configuration 1: create one endpoint, storage-gateway and collection on a single machine indentified under 'PrimaryGlobusNode'
- Configuration 2: create secondary nodes for load balancing the 'PrimaryGlobusNode'
- Configuration 3: create another endpoint, storage-gateway and collection supporting an internal private network. Referred to as the 'globusresearchnetwork'

Where required for your setup, alter the inventory to override the role default values.

Before running the playbooks review and update the ansible roles, playbook and inventory for your site.
`Role Variables` are described at the bottom of this page and includes setup details.

### Configuration 1:

To run the playbook:

> ansible-playbook -v -i globusinventory -l PrimaryGlobusNode -t m3_globus_part1 globusnodes.yml --ask-vault-pass

You will be prompted to enter the password for ansible-vault.
This will allow Ansible to decrypt the 'globus_clientSecret' during installation.

After this role has successfully completed, please action the last message. You
will need to login to the target machine and run 'globus-connect-server login
localhost'.

Once globus-connect-server has been logged in to the localhost, please run the
second role. This role will setup the storage-gateway and collection.

> ansible-playbook -v -i globusinventory -l PrimaryGlobusNode -t m3_globus_part2 globusnodes.yml --ask-vault-pass

.. note::

    Occasionally a http error 502 (Bad gateway) is returned when creating the
    'collection' for the task m3_globus_part2.

    To fix this login to the machine:
      `sudo globus-connect-server storage-gateway list`
      Using the storage-gateway ID, delete it
      `sudo globus-connect-server storage-gateway delete ID`

    Then re-run the second role. This will recreate the storage-gateway and the
    collection. The ID of the storage-gateway is required to create the collection.
    Alternatively, manually run the command for creating the collection. All
    values can be obtained from the Ansible output.

### Configuration 2:

If your Globus node is to be installed on several machines for load balancing run configuration 2 next.

> ansible-playbook -v -i globusinventory -l SecondaryGlobusNodes globusnodes.yml --ask-vault-pass

Ensure you can ssh between machines. This play will attempt to rsync the file 'deployment-key.json'
from the primary globus node across to the secondary globus node.

### Configuration 3:

Configuration 3 is the same as configuration 1, but with some of the configuration values overridden.

You will need to create an new client ID and client secret as this is a completely separate node. See `Role Variables`
below on how to obtain these.

Update the `globusinventory` file to override any required values in the role to distinguish the deployment
of this ResearchNode from the MainNode. In the sample provided the following values have been overridden: 'globus_clientId', 'globus_clientSecret',
'storage_gateway_DisplayName', and 'collection_DisplayName'.

To execute, run as separate commands, just like for configuration 1. Don't forget to login to Globus on the host prior to running 
the second role.

> ansible-playbook -v -i globusinventory -l ResearchNetworkNode -t m3_globus_part1 globusnodes.yml --ask-vault-pass

> ansible-playbook -v -i globusinventory -l ResearchNetworkNode -t m3_globus_part2 globusnodes.yml --ask-vault-pass

Cleaning up an Installation
---------------------------

```
WARNING: if you are planning on removing a Globus V5.4 installation, complete the following first. 
Otherwise you can be left with orphaned Endpoints and Collections in the web application that you
cannont remove on your own.
```

During the development of these Ansible scripts, unfortunately some orphaned Endpoints and Collections were created
that couldn't be removed. Globus Support was contacted to assist with this.

To prevent this problem the following commands will perform the cleanup for you.

1) Run the following command on all nodes in the endpoint:

    `globus-connect-server node cleanup`
    
2) Run the following command once on any node in the endpoint after step 1 is complete:

    `globus-connect-server endpoint cleanup --client-id YOUR_CLIENT_ID --deployment-key /path/to/your/deployment-key.json`


Role Variables
--------------

The following variables should be set prior to running the role m3_globus_part1.

- m3_globus_part1/defaults/main.yml
  - globus_clientId: clientID
  - globus_clientSecret: clientSecret

It is recommended that the globus_clientId and globus_clientSecret be set in the 'globusinventory' file.
The inventory file overrides role defaults. The same client ID and secret is required for configurations 1 and 2.
A new client ID and secret is required for configuration 3.

> NOTE: To obtain the clientID and clientSecret:
> - open https://developers.globus.org
> - click on 'Register a new Globus Connect Server v5'
> - Add another project.
> - For that new project, click on 'Add New Globus Connect Server'. This will display the Client ID.
> - Click on 'Generate New Client Secret'. This will display the 'Client Secret'
> - encrypt the 'Client Secret' using the below instructions


> NOTE: the variable ```globus_clientSecret``` should be encrypted using
> ```ansible-vault``` when setting up this role. This will ensure that the
> Client Secret is not accidentally shared.
>
> To encrypt your client secret: ```ansible-vault encrypt_string yourSecretGoesHere```
>
> When prompted enter the password to encrypt the string.
> The output is the encrypted Client Secret.
> Copy this into globus-auth.yml
>
> It should look like this.
>
```
globus_clientSecret: !vault |
                     $ANSIBLE_VAULT;1.1;AES256
                     66386449653236336462626566653063336164663966303231363934653561363064363833313662
                     6643162536303530376336343832656537303632313433360a626438346336353331386135323734
                     62656361653630373231613662633962316233633936396165386439616533353965373339616234
                     3430613539666330390a313736323265656432366236633330313963326365653937323833366536
                     34623731376664623134383463316265643436343438623266623965636363326136
```
> When running the playbook, use the option ```--ask-vault-pass```. This will
> prompt Ansible to ask for the password to decrypt your Globus password.

- m3_globus_part1/defaults/main.yml
  - endpoint_DisplayName: the name of your Endpoint.
  - endpoint_Organization: the organisation responsible for the Endpoint.
  - endpoint_Owner: globus login email address.
  - endpoint_DeploymentKeyPath: "deployment-key.json", the full path can be
  specified.

The following variables should be set prior to running the role m3_globus_part2.

- m3_globus_part2/defaults/main.yml
  - globus_subscription: if you have a Globus Subscription that is attached to
  the endpoint_Owner set this the 'True', otherwise 'False'
  - storage_gateway_DisplayName: the name of your storage gateway
  - storage_gateway_AuthDomains: the list of domains used for user authentication
  - storage_gateway_TimeOut: the time period that a gateway should be activated
  for, once authenticated e.g.  "$((60 * 24 * 5))" i.e. 5 days.
  - storage_gateway_DestinationPathRestrictions: This is the destination where
  the file 'path-restrictions.json', is copied on the target machine. This file
  should be customised for your requirements. Please refer to: https://docs.globus.org/globus-connect-server/v5.4/data-access-guide/#data_access_policies
  - storage_gateway_RestrictPaths: the full path on the target machine to the file
  'path-restrictions.json'. e.g. "file:/home/ec2-user/path-restrictions.json"
  - storage_gateway_UserDeny: Used to disable system users. e.g. "--user-deny root"
  - storage_gateway_HighAssurance: is the storage gateway high assurance? Requires a subscription.
  - storage_gateway_MFA: is MFA required on the gateway?
  - collection_BasePath: "/"
  - collection_DisplayName: the name of your collection
  - collection_Organization: the organisation responsible for the collection
  - collection_ContactEmail: contact email address
  - collection_InfoLink: A URL link to information on your collection
  - collection_Description: a description for you collection
  - collection_Keywords: any key words in a comma separated list.
  - collection_DestinationPathRestrictions: This is the destination where
  the file 'sharing-restrictions.json' is copied on the target machine. This file
  should be customised for your requirements. Please refer to: https://docs.globus.org/globus-connect-server/v5.4/data-access-guide/#sharing_configuration
  - collection_SharingRestrictPaths: the full path on the target machine to the file 'sharing-restrictions.json' e.g. "file:/home/ec2-user/sharing-restrictions.json"
  - collection_SharingGroupAllow: A unix group name whose members are allow to share data. e.g. "globusallow"
  - collection_SharingGroupDeny: A unix grop whose members are denied access to share data e.g. "globusdeny"
  - collection_UserMessage: a welcome message for the collection
  - collection_UserMessageLink: A URL that may be helpful to users of the collection.

  Note: To use Sharing, your Globus Endpoint needs to be 'managed' under a Globus subscription. Please refer to the Globus Connect Server installation notes on 'Sharing' for a full explanation.

These files will need customising for your site:
- m3_globusv5_part2/files/path-restrictions.json (update for your site requirements)
- m3_globusv5_part2/files/sharing-restrictions.json  (update for your site requirements)

The above configuration is an example. Please read the following to better understand Globus installation and customisation options.

- Data Access Guide:  https://docs.globus.org/globus-connect-server/v5.4/data-access-guide/
- Domain Guide:       https://docs.globus.org/globus-connect-server/v5.4/domain-guide/
- HTTPS Access to Collections: https://docs.globus.org/globus-connect-server/v5.4/https-access-collections/
- Identity Mapping Guide: https://docs.globus.org/globus-connect-server/v5.4/identity-mapping-guide/
- Globus OIDC Guide:  https://docs.globus.org/globus-connect-server/v5.4/globus-oidc-guide/


Author Information
------------------

Jay van Schyndel - Monash eResearch Centre
