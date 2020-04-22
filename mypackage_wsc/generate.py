#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
import argparse
from subprocess import check_output, STDOUT
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

def get(nom, region, whichip):
    ip = 'aws autoscaling describe-auto-scaling-instances --region {region} \
    --output text --query "AutoScalingInstances[?AutoScalingGroupName==\'{}\'].InstanceId "\
    | xargs -n1 aws ec2 describe-instances --instance-ids $ID --region {region} \
    --query Reservations[].Instances[].{}IpAddress --output text'.format(
        nom, whichip, region=region)

    output = check_output(ip, shell=True, stderr=STDOUT)
    ips = output.decode("utf-8")
    return ips


def main(group, env):

    bastion_public_ip = get("bastion", "eu-west-1", "Public")

    tpl_dir = Environment(loader=FileSystemLoader('./templates/'))

    template_cfg = tpl_dir.get_template('ansible-cfg.j2')


    template_ssh = tpl_dir.get_template('ssh-cfg.j2')


    template_in = tpl_dir.get_template('inventory.j2')


    nginx_ips = get("nginx", "eu-west-1", "Private")
    nginx_ips = nginx_ips.split("\n")

    tpl_cfg_output = template_cfg.render(group=group, env=env)
    tpl_ssh_output = template_ssh.render(group=group, env=env, bastion_public_ip=bastion_public_ip, nginx_ips=nginx_ips)
    tpl_invt_output = template_in.render(group=group, env=env, bastion_public_ip=bastion_public_ip, nginx_ips=nginx_ips)
    try:
        with open('./ansible.cfg', "w") as f:
            f.write(tpl_cfg_output)
            logger.info("ansible.cfg generated")
    except:
        logger.error("Failed to save file")
        sys.exit(1)
    try:
        with open('./configs/{}/{}/ansible/ssh.cfg'.format(group, env), "w") as f:
            f.write(tpl_ssh_output)
            logger.info("ssh file generated")
    except:
        logger.error("Failed to save file")
        sys.exit(1)
    try:
        with open('./configs/{}/{}/ansible/inventory'.format(group, env), "w") as f:
            f.write(tpl_invt_output)
            logger.info("inventory generated")
    except:
        logger.error("Failed to save file")
        sys.exit(1)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=" get ips")
    parser.add_argument('--group', help="group")
    parser.add_argument('--env', help="env")
    args = parser.parse_args()
    try:
        group = str(args.group)
        env = str(args.env)

    except NameError:
        sys.exit(1)
    except IndexError:
        sys.exit(1)
    main(group, env)
