AWS Naming convention
---------------------

Main considerations
~~~~~~~~~~~~~~~~~~~

Our conventions are described here ,The main terms we will use are :

- group = a logical whole to define the context where we are working (example : wsc).
- env = the iteration of the infrastructure for different puposes, values are : dev, staging, prod.
- aws_account = terraform_workspace.
- availibility_zone = the az, with this format : "eu-west-1a".
- scope = it is a free field to be coherent with the context we want to define for resources (example : the application perimeter for a subnet).
- The other variables are defined in the code, but not applicable to resources names in AWS.

The main rule is pretty simple, the name of a resource should be composed like that (with some exceptions, that's why there is a list in completion) :

::

    {group}-{env}-[{scope}]-{resource_name}


List of resources
~~~~~~~~~~~~~~~~~

VPC
^^^

::

    {group}-{env}-{scope}-vpc

    example : wsc-dev-vpc1-vpc

Subnet
~~~~~~

::

    {group}-{env}-{availibility_zone}-{scope}-{public|private}

    example : wsc-dev-eu-west-1b-myapp-public


Route tables
~~~~~~~~~~~~

::

    {group}-{env}-[{availibility_zone}]-{scope}-{routetype}-rt

    routetype values :
    public : when the rt has a route to internet gateway, instances access directly to internet using public ips.

    private : when the rt has a route to nat gateway, instances don't have external access, they don't have public ips.

    example : wsc-dev-eu-west-1b-myapp-private-rt

NAT Gateway
~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-ngw

    example : wsc-dev-ngw

Internet Gateway
~~~~~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-igw

    example : wsc-dev-nginx-igw

Application Load Balancer
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-alb

    example : wsc-dev-myapp-alb

Elastic Load Balancer (classic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-elbv1

    example : wsc-dev-myapp-elbv1

Target Group
~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-tg

    example : wsc-dev-myapp-tg

Elastic IP
~~~~~~~~~~

::

    {group}-{env}-[{availibility_zone}]-[{scope}]-eip

    example : wsc-dev-eu-west-1b-myapp-eip

Launch Template
~~~~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-lt

    example : wsc-dev-bastion-lt

Launch Configuration
~~~~~~~~~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-lc

    example : wsc-dev-myapp-lc

AutoScaling Group
~~~~~~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]-asg

    example : wsc-dev-myapp-asg

Security Group
~~~~~~~~~~~~~~

::

    {group}-{env}-[{region}]-[{scope}]-sg

    example : wsc-dev-myapp-sg

EC2 Instance
~~~~~~~~~~~~

::

    {group}-{env}-[{scope}]

    example : wsc-dev-myapp

Key pair
~~~~~~~~

::

    {firstname}.{lastname}

    example : kerbedj.mehdi

S3 Bucket
~~~~~~~~~

::

    {group}-{env}-{region}-[{scope}]

    example : wsc-dev--eu-west-1-tfstate

Dynamodb
~~~~~~~~

::

    {group}-{env}-{region}-[scope]

    example: wsc-dev-nginx-lock

