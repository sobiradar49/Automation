import sys
import yaml
import os
import time
import subprocess
import input_var
import datetime
from datetime import datetime
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


path = input_var.path
cluster_ip = input_var.cluster_ip
old_image_version = input_var.old_image_version
new_image_version = input_var.new_image_version
n2_ip = input_var.n2_ip
n6_pci = input_var.n6_pci
n3_pci = input_var.n3_pci
old_buildpath = input_var.old_buildpath
Clear_data_from_mnt_folders = input_var.Clear_data_from_mnt_folders
Cluster_reset = "no"
nef_ee = input_var.nef_ee
nef_pp = input_var.nef_pp
#kubernetes_image_version = input_var.kubernetes_image_version
#kubernetes_build_path = input_var.kubernetes_build_path
nef = input_var.nef
sriov = input_var.sriov

file_load_10 ='ingress-1-values.yaml'
file_load_11 ='ps-1-values.yaml'
file_load_13 = 'global-values.yaml'
file_load_14 = 'cluster-config.yaml'
file_load_16 = 'nef-1-values.yaml'


def exec_cmd(cmd):
    # Execute in a sub-process and capture output.
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = proc.communicate()

    return stdout.decode("utf-8") + stderr.decode("utf-8")


print(Fore.BLUE+"\n Clear data from mnt folders based on user input \n")
cleardb = clear_db()

