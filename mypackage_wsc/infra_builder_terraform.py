"""
Infra bootstrap

"""
import argparse
import os
import sys
from subprocess import check_output, STDOUT
import logging
import boto3

# Get All regions

default_ec2 = boto3.client('ec2')
enabled_regions = set(r['RegionName'] for r in default_ec2.describe_regions()['Regions'])

# Logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# Terraform init Function

def init_layer(layer, region, account, provider, target_bucket):
    """
    Initiation layer

    """
    logger.info("Initalize layer %s \n \n ", layer)
    command_init = "terraform init -backend-config region={region}\
    -backend-config dynamodb_table={}-{region}-tfstate-lock\
    -backend-config bucket={}\
    -backend-config key={}.tfstate\
    -force-copy".format(account, target_bucket, layer, region=region)
    os.chdir("{}{}/{}/".format(layer_path, provider, layer))
    os.system(command_init)

# Terraform Action function


def execute_layer(layer, region, account, provider, target_bucket, action, config_dir, options):
    """
    Execute Layer

    """
    command_apply = "terraform {} {} \
    -var-file={config_dir}/commons.tfvars \
    -var-file={config_dir}/layer-{}.tfvars".format(action, options, layer, config_dir=config_dir)
    init_layer(layer, region, account, provider, target_bucket)
    logger.info("Execute Layer\n \n")
    os.system(command_apply)


def main(args):
    """
    Main
    """
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Build infra script")
    # Add the parameters positional/optional
    parser.add_argument('--account', help="account <group>-<env>")
    parser.add_argument('--action', help="plan apply or destroy", default="apply")
    parser.add_argument('--region', help="eu-west-1 by default", default="eu-west-1")
    parser.add_argument('--layer', help="terraform layer")
    parser.add_argument('--ignore', nargs='*', help="terraform layer you want to ignore it")
    parser.add_argument('--provider', help="cloud provider , by default aws", default="aws")
    parser.add_argument('--approve', help="Auto-approve option ,set 'yes' to enable it ")

    # Parse the arguments
    args = parser.parse_args()
    account = str(args.account)
    action = str(args.action)
    region = str(args.region)
    layer = str(args.layer)
    ignor = args.ignore
    provider = str(args.provider)
    auto = str(args.approve)
    options = ""
    target_bucket = "{}-{}-tfstate".format(account, region)
    command_find = "ls -1 {}{}".format(layer_path, provider)
    output = check_output(command_find, shell=True, stderr=STDOUT)
    Layers = str(output.decode("utf-8"))
    Layers = Layers.split("\n")
    check_argument = True

    if args.account is None:

        logger.error("Missing account argument,Wedeployer Can not run without Account")
        sys.exit(1)

    try:

        account_name = args.account
        account_split = account_name.split("-")
        group = account_split[0]
        env = account_split[1]

    except NameError:

        logger.error("Error no account argument")
        sys.exit()

    except IndexError:

        logger.error("Error in syntax argument")
        sys.exit()

    except AttributeError:

        logger.error("No attribute argumFileNotFoundError:ent")
        sys.exit()

    if action not in ("apply", "plan", "destroy"):

        logger.error("Error ,Bad Action for Terraform,just 'apply','plan' and 'destroy' are available")
        check_argument = False

    if region not in enabled_regions:

        logger.error("No Region Found with this Name")
        check_argument = False

    if auto == "yes":

        options = "-auto-approve"

    elif auto != "None":

        logger.error("Error , Auto-Approve is disabled by default ,it takes only 'yes'")

    if check_argument is False:

        logger.info("You must fix errors mentioned above")
        sys.exit(1)

    config_dir = "./../../../../configs/{}/{}/terraform".format(group, env)
    target_bucket = "{}-{}-tfstate".format(account, region)
    command_find = "ls -1 {}{}".format(layer_path, provider)
    check_layer = layer in Layers

    if check_layer is False:

        if layer == "None":
            logger.error("No layer Argument passed ")

        else:
            logger.error("Error in layer argument")

    else:
        execute_layer(layer, region, account, provider, target_bucket, action, config_dir, options)
        sys.exit()


    if layer == "None" and action in ('apply', 'plan'):

        logger.info("#############= No Layer Found in Argument , we will run all Layers ====#####################\n")
        for sublayer in Layers:
            try:
                ignored_layer = ignor[Layers.index(sublayer)]
            except IndexError:
                ignored_layer = ""
            except TypeError:
                ignored_layer = ""
            if sublayer not in ('', ignored_layer):
                execute_layer(sublayer, region, account, provider, target_bucket, action, config_dir, options)
                os.chdir("../../../../")


    elif action == "destroy":
        command_find = "ls -1r {}{}".format(layer_path, provider)
        command_find = str(command_find)
        output = check_output(command_find, shell=True, stderr=STDOUT)
        Layers = str(output.decode("utf-8"))
        Layers = Layers.split("\n")
        for sublayer in Layers:
            try:
                ignored_layer = ignor[Layers.index(sublayer)]
            except IndexError:
                ignored_layer = ""
            except TypeError:
                ignored_layer = ""
            if sublayer not in ('', ignored_layer):
                execute_layer(sublayer, region, account, provider, target_bucket, action, config_dir, options)
                os.chdir("../../../../")


if __name__ == '__main__':
    layer_path = "./terraform/layers/"
    default_ec2 = boto3.client('ec2')
    enabled_regions = set(r['RegionName'] for r in default_ec2.describe_regions()['Regions'])
    main(sys.argv[1:])
