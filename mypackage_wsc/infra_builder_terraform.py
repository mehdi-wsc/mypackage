import argparse
import os
import sys
from subprocess import check_output, STDOUT
import logging


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()

stream_handler.setLevel(logging.INFO)

logger.addHandler(stream_handler)

layer_path = "./terraform/layers/"



### Terraform init Function

def init_layer(layer, region, account, provider, target_bucket):
    logger.info("Initalize layer %s \n \n ", layer)

    command_init = "terraform init -backend-config region={region}\
    -backend-config dynamodb_table={}-{region}-tfstate-lock\
    -backend-config bucket={}\
    -backend-config key={}.tfstate\
    -force-copy".format(account, target_bucket, layer, region=region)

    os.chdir(layer_path+provider+"/"+layer+"/")

    os.system(command_init)


### Terraform Action function

def execute_layer(layer, region, account, provider, target_bucket, action, config_dir, options):
    command_apply = "terraform {} {} \
    -var-file={config_dir}/commons.tfvars \
    -var-file={config_dir}/layer-{}.tfvars".format(action, options, layer, config_dir=config_dir)
    init_layer(layer, region, account, provider, target_bucket)
    logger.info("Execute Layer\n \n")
    os.system(command_apply)



def main(args):
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Build infra script")

    # Add the parameters positional/optional
    parser.add_argument('--account', help="account <group>-<env>")
    parser.add_argument('--action', help="plan apply or destroy", default="apply")
    parser.add_argument('--region', help="eu-west-1 by default", default="eu-west-1")
    parser.add_argument('--layer', help="terraform layer")
    parser.add_argument('--ignore', nargs='*', help="terraform layer you want to ignore it")
    parser.add_argument('--provider', help="cloud provider , by default aws", default="aws")
    parser.add_argument('--approve', help="Auto-approve option ")

    # Parse the arguments
    provider = None
    group = None
    env = None
    args = parser.parse_args()
    provider = args.provider
    region = args.region
    auto = args.approve

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
        logger.error("No attribute argument")
        sys.exit()


    if auto == "yes":
        options = "-auto-approve"
    else:
        options = ""


    config_dir = "./../../../../configs/"+group+"/"+env+"/""terraform"

    account = args.account

    action = args.action

    region = args.region

    layer = args.layer

    ignor = args.ignore

    target_bucket = account+"-"+region+"-tfstate"

    layer_path = "./terraform/layers/"

    command_find = "ls -1 "+layer_path+ provider

    command_find = str(command_find)


    output = check_output(command_find, shell=True, stderr=STDOUT)



    Layers = str(output.decode("utf-8"))

    Layers = Layers.split("\n")

    layer = str(layer)

    check_layer = layer in Layers

    if check_layer == False:

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
        command_find = "ls -1r "+layer_path+ provider
        command_find = str(command_find)
        output = check_output(command_find, shell=True, stderr=STDOUT)
        Layers = str(output.decode("utf-8"))
        Layers = Layers.split("\n")
        for sublayer in Layers:

            if sublayer != "":
                execute_layer(sublayer, region, account, provider, target_bucket, action, config_dir, options)
                os.chdir("../../../../")

if __name__ == '__main__':

    main(sys.argv[1:])
