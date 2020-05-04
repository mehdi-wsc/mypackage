"""
Remove .Terraform folders
"""
import os

command = "find . -name .terraform -type d -exec rm -rf {} \;"
os.chdir("terraform/")
os.system(command)
