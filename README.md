# mypackage_wsc

mypackage_wsc is Python package to automate deploiment of infrastructure. Writtent and compatible with python 3 .
to use mypackage_wsc you should follow Wedeployer skeletton.

## Documentation

 Documentation to Wedeployer skeletton
 <br>
<https://infra-doc.readthedocs.io/en/latest/>
</br>

## installation

Using pip, the Python package manager:

```
pip install --user mypackage_wsc==0.0.7
```

mypackage_wsc is developed for Linux os , No windows version is available.

## Usage

mypackage_wsc automate terraform initialization and deploiment ,although generating necessary files for ansible and launch playbook.<br>
I will describe below simple usage.

- mypackage_wsc.infra_bootstrap:

```
python -m mypackage_wsc.infra_bootstrap --account <group>-<env>
```

- mypackage_wsc.infra_builder_terraform:

```
python -m mypackage_wsc.infra_builder_terraform --account <group>-<env>
```

- mypackage_wsc.install_nginx:

```
python -m mypackage_wsc.install_nginx --group <group>-<env>
```

## Features

Here are features for infra_builder_terraform script:

```
Builder Terraform Script:
optional arguments:
  -h, --help            show this help message and exit
  --account ACCOUNT     account <group>-<env>
  --action ACTION       plan apply or destroy
  --region REGION       eu-west-1 by default
  --layer LAYER         terraform layer
  --ignore              ignore layer
  --provider PROVIDER   cloud provider , by default aws
  --approve APPROVE     Auto-approve option ,set 'yes' to enable it
```

Here are features for infra_bootstrap script :

```
Boot Strap script

optional arguments:
  -h, --help           show this help message and exit
  --provider PROVIDER  provider aws
  --account ACCOUNT    account <group>-<env>
  --action ACTION      plan apply or destroy
  --region REGION      eu-west-1 by default
  --approve APPROVE    Auto-approve option ,set 'yes' to enable it
```

## license

[GNU GENERAL PUBLIC LICENSE](https://github.com/mehdi-wsc/mypackage/blob/master/LICENSE)