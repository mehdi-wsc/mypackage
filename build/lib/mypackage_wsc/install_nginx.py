import os
import argparse
import logging
from mypackage_wsc import generate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

def main(group, env):
    """
    Main
    """
    if group is None or env is None:
        logger.error("\nNo arguments passed\n")
        logger.warning("Please to run ansible you should pass your group and environnement in arguments\n")
        logger.warning('Syntax : python wedeployer/install-nginx.py --group <group> --env <environnement>\n')
    else:
        generate.main(group, env)
        command_ansible = "ansible-playbook ansible/main.yml"
        os.system(command_ansible)
if __name__ == '__main__':
   # Initialize the parser
    parser = argparse.ArgumentParser(description="Ansible playbook run ")
    # Add the parameters positional/optional
    parser.add_argument('--group', help="group")
    parser.add_argument('--env', help="env")
    args = parser.parse_args()
    grp = args.group
    environment = args.env
    main(grp, environment)
