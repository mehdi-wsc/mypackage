"""
    Bootstrap script init

"""
import argparse
import os
import sys
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()

stream_handler.setLevel(logging.INFO)

logger.addHandler(stream_handler)



def main(action, options, group, env, region, provider):
    config_dir = "./../../../configs/"+group+"/"+env+"/""terraform"
    command_init = "terraform init"
    command_apply = "terraform {} {} -var=group={}\
    -var=env={} -var=region={key} -state={}/bootstrap-{}-{key}.tfstate".format(
        action, options, group, env, config_dir, provider, key=region)
    bootstrap_dir = "./terraform/bootstrap/aws"

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
    # Parse the arguments
    args = parser.parse_args()

    action = args.action
    region = args.region

    if args.provider == 'aws' or args.provider == 'gcp':
        provider = args.provider
    else:
        print("Error in provider argument")

        sys.exit()
    try:
        txt = args.account
        x = txt.split("-")
        group = x[0]
        env = x[1]
    except NameError:
        logger.error("Error no account argument")
        sys.exit()
    except IndexError:
        logger.error("Erro in syntax argument")
        sys.exit()
    except AttributeError:
        logger.error("No argument passed")
        sys.exit()

    if args.action == "apply" or args.action == "destroy":
        options = "-auto-approve"
    elif args.action == "plan":
        options = "-detailed-exitcode"
    main(action, options, group, env, region,provider)
