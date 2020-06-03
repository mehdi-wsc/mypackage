"""
genrate configuration files
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
import os
import argparse
from subprocess import check_output, STDOUT
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

def get(nom, region, whichip):
    """
    get method

    """
    ip = 'aws autoscaling describe-auto-scaling-instances --region {region} \
    --output text --query "AutoScalingInstances[?AutoScalingGroupName==\'{}\'].InstanceId "\
    | xargs -n1 aws ec2 describe-instances --instance-ids $ID --region {region} \
    --query Reservations[].Instances[].{}IpAddress --output text'.format(
        nom, whichip, region=region)

    output = check_output(ip, shell=True, stderr=STDOUT)
    ips = output.decode("utf-8")
    return ips


def main(group, env):
    """
    Main

    """
    bastion_public_ip = get("{}-{}-bastion-asg".format(group, env), "eu-west-1", "Public")
    workdir = os.getcwd()
    tpl_dir = Environment(loader=FileSystemLoader('{}/templates/'.format(workdir)))
    template_cfg = tpl_dir.get_template('ansible-cfg.j2')
    template_ssh = tpl_dir.get_template('ssh-cfg.j2')
    template_in = tpl_dir.get_template('inventory.j2')
    nginx_ips = get("{}-{}-nginx-asg".format(group, env), "eu-west-1", "Private")
    nginx_ips = nginx_ips.split("\n")

    if nginx_ips == ['']:
        logger.error("Nginx IPs not found, verify your auto-scaling group ")

    if bastion_public_ip == "":
        logger.error("Bastion Ip not found , verify your auto-scaling group ")
        sys.exit(1)

    tpl_cfg_output = template_cfg.render(group=group, env=env)
    tpl_ssh_output = template_ssh.render(group=group, env=env, bastion_public_ip=bastion_public_ip, nginx_ips=nginx_ips)
    tpl_invt_output = template_in.render(group=group, env=env, bastion_public_ip=bastion_public_ip, nginx_ips=nginx_ips)

    try:
        with open('./{}-{}-ansible.cfg'.format(group, env), "w") as f:
            f.write(tpl_cfg_output)
            logger.info("ansible.cfg generated")

    except FileNotFoundError:
        logger.error("Failed to save file")
        sys.exit(1)

    try:
        with open('./configs/{}/{}/ansible/ssh.cfg'.format(group, env), "w") as f:
            f.write(tpl_ssh_output)
            logger.info("ssh file generated")
    except FileNotFoundError:
        logger.error("Failed to save file")
        sys.exit(1)

    try:
        with open('./configs/{}/{}/ansible/inventory'.format(group, env), "w") as f:
            f.write(tpl_invt_output)
            logger.info("inventory generated")
    except FileNotFoundError:
        logger.error("Failed to save file")
        sys.exit(1)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=" get ips")
    parser.add_argument('--group', help="group")
    parser.add_argument('--env', help="env")
    args = parser.parse_args()
    if args.group is None or args.env is None:
        logger.error("Missing argument , please verify help for more informations")
        sys.exit(1)
    try:
        grp = str(args.group)
        environment = str(args.env)

    except NameError:
        sys.exit(1)
    except IndexError:
        sys.exit(1)
    main(grp, environment)
