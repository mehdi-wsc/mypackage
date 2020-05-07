"""
Infra bootstrap

"""
import argparse
import os
import sys
import logging
import boto3

default_ec2 = boto3.client('ec2')
enabled_regions = set(r['RegionName'] for r in default_ec2.describe_regions()['Regions'])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
check_argument = True

def main(action, options, group, env, region, provider):
    """
    main
    """

    config_dir = "./../../../configs/{}/{}/terraform".format(group, env)
    bootstrap_dir = "./terraform/bootstrap/{}".format(provider)
    command_init = "terraform init"
    command_apply = "terraform {} {} -var=group={}\
    -var=env={} -var=region={key} -state={}/bootstrap-{}-{key}.tfstate".format(
        action, options, group, env, config_dir, provider, key=region)
    os.chdir(bootstrap_dir)
    os.system(command_init)
    os.system(command_apply)

if __name__ == '__main__':
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Boot Strap script ")
    # Add the parameters positional/optional
    parser.add_argument('--provider', help="provider aws", default="aws")
    parser.add_argument('--account', help="account <group>-<env>")
    parser.add_argument('--action', help="plan apply or destroy", default="apply")
    parser.add_argument('--region', help="eu-west-1 by default", default="eu-west-1")
    parser.add_argument('--approve', help="Auto-approve option ,set 'yes' to enable it")
    # Parse the arguments
    args = parser.parse_args()
    act = args.action
    reg = args.region
    opt = ""
    if args.provider == 'aws' or args.provider == 'gcp':
        pro = args.provider
    else:
        logger.error("Error in provider argument")
        sys.exit()
    if args.account is None:
        logger.error("Missing account argument,Wedeployer Can not run without Account")
        sys.exit(1)
    try:
        account_name = args.account
        account_name = account_name.split("-")
        grp = account_name[0]
        environment = account_name[1]
    except IndexError:
        logger.error("Error in syntax argument")
        sys.exit()
    except AttributeError:
        logger.error("Attribute Error")

    if act not in ("apply", "plan", "destroy"):
        logger.error("Error ,Bad Action for Terraform,just 'apply','plan' and 'destroy' are available")
        check_argument = False

    if reg not in enabled_regions:
        logger.error("No Region Found with this Name")
        check_argument = False
    if args.approve == "yes":
        opt = "-auto-approve"
    elif args.approve is not None:
        logger.error("Error , Auto-Approve is disabled by default ,it takes only 'yes'")

    if check_argument is True:
        main(act, opt, grp, environment, reg, pro)
    else:
        logger.info("You must fix errors mentioned above")
        sys.exit(1)
