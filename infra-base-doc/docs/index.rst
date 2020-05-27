Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   quickstart
   naming
   tagging


wedeployer skelleton Documentation
==================================


Introduction
------------

wedeployer skelleton is structure of folders  ,it has been made to facilitate the building , deploiment and configuration of the infrastructure.

Benefits
--------

- wedeployer skelleton allows you to launch wedeployer python package.
- you can use Docker workstation.
- high structure which facilitates  debugging problems.

wedeployer package
------------------
- wedeployer github page:

` Github wedployer repo <https://github.com/mehdi-wsc/mypackage>`_

Terraform structure
-------------------

tree below describes the required organization to set files:

::

    ├── terraform
    │   ├── bootstrap
    │   │   └── <provider>/(tf files)
    │   ├── layers
    │   │   └── <provider>
    │   │       ├── 01-<name of first layer>/(tf files)
    │   │       └── 02-<name of second layer>/(tf files)

- bootstrap: is folder where to store bootstap scenario for example ( create s3 bucket and dynamodb to store tfstate).
- layers: is folder where to store your stack terraform layers.
- After bootstrap and layers you should specify the provider.
- Name of layer should be : xx-<name of layer>(with xx from 00 to 99).

configuration structure
-----------------------
To set the configuration for your account,

There is an example of configuration here :

::

        configs
        └── mygroup
            └── myenv
                ├── ssh
                │   └── README.md
                ├── ansible
                │   ├── inventory
                │   └── ssh.cfg
                └── terraform
                    ├── commons.tfvars
                    └── layer-xx-<name of layer>.tfvars

To adapt to your own account and set your own values,

just copy paste the folder "mygroup", and change the names of the folders :

- mygroup: is a logical entity that represent your context (for instance : "mycompany").
- myenv: is the iteration of the infrastructure dedicated to a purpose (for instance : "dev", "staging" or "prod").
- Terraform tfvars: the name of file  should be layer-xx-<name of layer>.tfvars.
- Ansible configs: you set ssh.cfg and inventory.


ansible structure
-----------------

ansible structure is simple , in your root create ansible folder and set your main.yml inside it, like below:

::

    ansible
      ├── main.yml
      └── roles
           └── external

and specify roles in roles subdirectory.

configuration and templates files
---------------------------------

- I had jinja2 templates to generate ansible configuration files (ssh.cfg ,inventory,ansible.cfg).

- you can already customize your templates files in :

::

    ./templates

Docker workstation
------------------

- You can define workstation to work in :

::

        workstation/
         ├── Dockerfile
         └── launch.sh

I already set Dockerfile and Script to launch it , however you can customize it.

Exemple configuration:
----------------------

::


    ├── ansible
    │   └── roles
    │       └── external
    │           └── mehdi_wsc.nginx
    ├── configs
    │   └── mygroup
    │       └── myenv
    │           ├── ansible
    │           ├── ssh
    │           └── terraform
    ├── templates
    ├── terraform
    │   ├── bootstrap
    │   │   └── aws
    │   └── layers
    │        └── aws
    │           ├── 01-networking
    │           └── 02-nginx
    └── workstation
        ├── Dockerfile
        └── launch.sh

- to understand how it works , we have infra-base  quickstart example:

:doc: `Quick start page <./quickstart.html>`_

