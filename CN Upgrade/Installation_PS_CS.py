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

def exec_cmduntar(cmd,path):
    # Execute in a sub-process and capture output.
    os.chdir(path)
    print(os.getcwd())
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = proc.communicate()

    return stdout.decode("utf-8") + stderr.decode("utf-8")


def clear_db():
    if Clear_data_from_mnt_folders.casefold() == "yes" or Clear_data_from_mnt_folders.casefold() == "y":
        isExist = os.path.exists("/mnt/data5")
        if isExist == False:
            os.mkdir("/mnt/data5")
        clear_db = exec_cmd("rm -rf /mnt/data0/*; rm -rf /mnt/data1/*; rm -rf /mnt/data2/*; rm -rf /mnt/data5/*")
        print(clear_db)
        print(Fore.RED+"\n Data has been cleared from mnt folders \n")
    else:
        print (Fore.GREEN+"\n Data hasn't been cleared from mnt floders \n")

def copy_load(basepath,path):
    # Execute in a sub-process and capture output.
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/common/tools/install")
    print(os.getcwd())
    proc = subprocess.Popen(
        basepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = proc.communicate()

    return stdout.decode("utf-8") + stderr.decode("utf-8")

def load_fun(new_image_version,path):
    os.chdir(path)
    print(os.getcwd())
    os.system('./load.sh {}' .format(str(new_image_version)))
    time.sleep(5)
def ps_ingress(cluster_ip,file_load,path,new_image_version):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/platform-services/scripts")
    with open (file_load) as read_file:
        node = yaml.safe_load(read_file)
        node['nginx-ingress']['nginx_ingress']['externalIP'] = cluster_ip
        with open(file_load, 'w') as yaml_file:
            data = yaml_file.write(yaml.dump(node, sort_keys=False, default_flow_style=False))
            file_load =data


def ps_el(cluster_ip,file_load,path,new_image_version):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/platform-services/scripts")
    with open (file_load) as read_file:
        node = yaml.safe_load(read_file)
        print(node)
        node['fluentd']['elasticHost'] = cluster_ip
        node['kibana']['elasticHost'] = cluster_ip
        with open(file_load, 'w') as yaml_file:
            data = yaml_file.write(yaml.dump(node, sort_keys=False, default_flow_style=False))
            file_load =data
def platform_services(path,new_image_version):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/platform-services/scripts")
    os.system("sh install_ps.sh")
    time.sleep(10)
    os.system("sh install_mongodb.sh")
    time.sleep(90)
    os.system("sh addmongoreplica.sh")
    time.sleep(25)
    os.system("sh addmongoreplica.sh")
    time.sleep(10)
    ns = exec_cmd("kubectl get ns")
    print(Fore.BLUE+ns)
    if "mongodb" and "radisys-ps1" and "ingress-nginx" in ns:
        print(Fore.BLUE+"\n Platform services are installed sucessfully \n")
    else:
        print(Fore.RED+"\n FAILED TO INSTALL PLATFORM SERVICES \n")
        exit()

def cs_function(file_load, default_nf_version, new_image_version,path):
        os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/common-services/scripts")
        fin = open(file_load, "rt")
        #read file contents to string
        data = fin.read()
        #replace all occurrences of the required string_function
        data = data.replace(default_nf_version, new_image_version)
        #close the input file
        fin.close()
        #open the input file in write mode
        fin = open(file_load, "wt")
        #overrite the input file with the resulting data
        fin.write(data)
        #close the file
        fin.close()

def common_service(path,new_image_version):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/common-services/scripts")
    os.system("sh install_cs.sh")
    time.sleep(1)
    ns = exec_cmd("kubectl get ns")
    print(Fore.BLUE+ns)
    if "radisys-cs1" in ns:
        print(Fore.BLUE+"\n Common services are installed sucessfully \n")
    else:
        print(Fore.RED+"\n FAILED TO INSTALL COMMON SERVICES \n")
        exit()

########################Clear data from mnt folders #######################
print(Fore.BLUE+"\n Clear data from mnt folders based on user input \n")
cleardb = clear_db()

########################Untar CNF file and nf images #######################
print(Fore.BLUE+"\n Starting the unzip process for new package \n")
untar = ("tar -xvf TRILLIUM_5GCN_CNF_REL_"+new_image_version+".tar.gz")
exec_cmduntar(untar,path)
basepath = "cp load.sh"+" "+path
print(Fore.BLUE+"\n Copying the load.sh script to base path \n")
copy_load(basepath,path)
print(Fore.BLUE+"\n Loading the new images \n")
load_fun(new_image_version,path)
########################PS installation #######################
print(Fore.BLUE+"\n Starting the Platform service installation \n")
ps_ingress(cluster_ip,file_load_10,path,new_image_version)
ps_el(cluster_ip,file_load_11,path,new_image_version)
platform_services(path,new_image_version)



######################## CS Installation #######################
print(Fore.BLUE+"\n Starting the Common service installation \n")
cs_function(file_load_9,default_nf_version,new_image_version,path)
common_service(path,new_image_version)
