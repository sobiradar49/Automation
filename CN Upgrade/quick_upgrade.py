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

file_load = 'ems-1-values.yaml'
file_load_1 = 'nrf-1-values.yaml'
file_load_2 = 'udsf-1-values.yaml'
file_load_3 = 'smf-1-values.yaml'
file_load_4 = 'udm-1-values.yaml'
file_load_5 = 'nssf-values.yaml'
file_load_6 = 'udr-1-values.yaml'
file_load_7 = 'amfv2-1-values.yaml'
file_load_8 = 'upf-1-values.yaml'
file_load_9 = 'cs-1-values.yaml'
file_load_10 ='ingress-1-values.yaml'
file_load_12 = 'ausf-1-values.yaml'
file_load_11 ='ps-1-values.yaml'
file_load_13 = 'global-values.yaml'
file_load_14 = 'cluster-config.yaml'
file_load_15 = 'elasticsearch.yml'
file_load_16 = 'nef-1-values.yaml'

default_nf_version = 'v1'


def date():
    now = datetime.now() # Use now() to access the current date and time
    print(Fore.YELLOW+"Current date and time is ", Fore.YELLOW+str(now))

def exec_cmd(cmd):
    # Execute in a sub-process and capture output.
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = proc.communicate()

    return stdout.decode("utf-8") + stderr.decode("utf-8")

def el_update(file_load,cluster_ip):
    os.chdir("/etc/elasticsearch")
    config = [("path.data:"," /var/lib/elasticsearch"),("path.logs:"," /var/log/elasticsearch"),("network.host: ", cluster_ip), ("transport.host:"," localhost"),("transport.tcp.port:"," 9300"),("http.port:"," 9200"),("ingest.geoip.downloader.enabled:", "false")]
    with open('elasticsearch.yml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in config))


def elastic_status(file_load,cluster_ip):
    el_status = ("systemctl status elasticsearch.service | head -3")
    elasticsearch = exec_cmd(el_status)
    print(elasticsearch)
    substring = "enabled"
    substring1 ="disabled"
    count= elasticsearch.count(substring)
    count1=elasticsearch.count(substring1)
    if count == 2:
        os.system("systemctl enable elasticsearch.service")
        os.system("systemctl status elasticsearch.service | head -3")
        print("Enabled elasticsearch service")
    elif count ==1 and count1 ==1:
        os.system("systemctl enable elasticsearch.service")
        os.system("systemctl status elasticsearch.service | head -3")
        print("Enabled elasticsearch service")
    else:
        os.system("apt-get install -y apt-transport-https")
        os.system("wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -")
        os.system("sudo apt install -y software-properties-common")
        os.system("echo deb https://artifacts.elastic.co/packages/7.x/apt stable main | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list")
        os.system("apt-get update -y")
        os.system("apt-get install -y elasticsearch")
        el_update(file_load,cluster_ip)
        os.system("systemctl restart elasticsearch.service")
        os.system("systemctl enable elasticsearch.service")
        os.system("systemctl status elasticsearch.service | head -3")
def cluster_reset(cluster_ip,kubernetes_image_version,kubernetes_build_path,file_load_14):
    if Cluster_reset.casefold() == "yes" or Cluster_reset.casefold() == "y":
        os.chdir('/root')
        print(Fore.BLUE+"\n Starting the cluster reset \n ")
        print(Fore.GREEN+"\n Please clik on enter to proceed cluster reset")
        cluster = os.system("ansible-playbook -i /root/kube/installation/cluster/hosts.yml /root/kube/installation/cluster/reset.yml")
        print(cluster)
        time.sleep(5)
        print(Fore.RED+"\n Performed the cluster_reset \n")
        ns = exec_cmd("kubectl get ns")
        print(Fore.BLUE+ns)
        if "istio-system" and "kube-system" in ns:
            print(Fore.RED+"\n FAILED TO UNINSTALL K8 SERVICES")
            exit()
        else:
            print(Fore.BLUE+"\n Uninstalled K8 SERVICES")
            cluster_bringup(cluster_ip,kubernetes_image_version,kubernetes_build_path,file_load_14)
    else:
        print (Fore.GREEN+"\n User don't want to delete K8 services \n")

def cluster_bringup(cluster_ip,kubernetes_image_version,kubernetes_build_path,file_load_14):
        os.chdir(path)
        print("Please click on enter to create ssh key")
        ssh_keyset= exec_cmd("ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa")
        print(ssh_keyset)
        ssh_cmdwithip = "ssh-copy-id root@"+cluster_ip
        ssh_keyset1= exec_cmd(ssh_cmdwithip)
        print(ssh_keyset1)
        ssh_keyset2 = exec_cmd("cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys")
        print(Fore.BLUE+"\n Starting the K8 service installation \n")
        common(cluster_ip,kubernetes_image_version,kubernetes_build_path,file_load_14)

def common(cluster_ip,kubernetes_image_version,kubernetes_build_path,file_load):
    os.chdir(kubernetes_build_path)
    os.system("tar -xvf TRILLIUM_CNF_PLATFORM_{}.tar.gz" .format(str(kubernetes_image_version)))
    os.chdir(kubernetes_build_path+"/platform/kubespray")
    with open (file_load) as read_file:
        node = yaml.safe_load(read_file)
        node["cluster_config"]["hosts"]["node1"]["ip"]= cluster_ip
        print(node)
        with open(file_load, 'w') as yaml_file:
           data = yaml_file.write(yaml.dump(node, sort_keys=False, default_flow_style=False))
           file_load = data
    cluster_ins(kubernetes_build_path)
def cluster_ins(kubernetes_build_path):
    os.chdir(kubernetes_build_path+"/platform/kubespray")
    print(os.getcwd())
    os.system("sed -i -e 's/\r$//' install_cluster.sh")
    os.system("bash install_cluster.sh")
    ns = exec_cmd("kubectl get ns")
    print(ns)
    if  "kube-system" in ns:
        print(Fore.BLUE+"\n K8 services are installed sucessfully \n")
    else:
        print(Fore.RED+"\n FAILED TO INSTALL K8 SERVICES")
        exit()
    time.sleep(1)


def getDfdes(cmd):
    df = os.popen(cmd)
    i =0
    while True:
        i = i+1
        line = df.readline()
        if i==1:
            return(line.split()[0:6])

def getDf(cmd):
    df = os.popen(cmd)
    i = 0
    while True:
        i = i+1
        line = df.readline()
        if i==2:
            return(line.split()[0:6])
def memdisk():
        ## if the disk usage is more than 70% then script will stop
        disk = "df -kh . /"
        description = getDfdes(disk)
        disk_root = getDf(disk)
        print(description)
        print(disk_root)
        op = description[4]+" : " + disk_root[4]

        if disk_root[4] <="70%":
                print (Fore.YELLOW+"Disk usage is less than 70% \n")
        else:
                print(Fore.RED+"\n Disk usage is more than threshold defined threshold \n")
                exit()

        #### Memory should be more than 32 GB
        mem = "cat /proc/meminfo"
        mem_1 = getDfdes(mem)
        mem_op = mem_1[0]+" : " + mem_1[1]
        print (mem_op)
        if mem_1[1] >= "32869772":
                print (Fore.YELLOW+"Memory allocated 32GB \n")
        else:
                exit()



def uninstall_nfservice(old_buildpath,old_image_version,nf):
                os.chdir(old_buildpath+"/TRILLIUM_5GCN_CNF_REL_"+old_image_version+"/nf-services/scripts/")

                os.system("sh uninstall_"+nf+".sh")
                time.sleep(1)


def uninstall_cmservice(old_buildpath,old_image_version):
                os.chdir(old_buildpath+"/TRILLIUM_5GCN_CNF_REL_"+old_image_version+"/common-services/scripts")
                os.system("sh uninstall_cs.sh")
                time.sleep(1)

def uninstall_psservice(old_buildpath,old_image_version, nm):
                os.chdir(old_buildpath+"/TRILLIUM_5GCN_CNF_REL_"+old_image_version+"/platform-services/scripts")
                if nm == "ps":
                        os.system("sh uninstall_ps.sh")
                        time.sleep(1)
                if nm == "mongodb":
                        os.system("sh uninstall_mongodb.sh")
                        time.sleep(1)

def uninstall():
        ns = exec_cmd("kubectl get ns")
        print(ns)

        if "radisys-upf1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"upf")

        if "radisys-smf1" in ns:
                 uninstall_nfservice(old_buildpath,old_image_version,"smf")

        if "radisys-nssf1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"nssf")

        if "radisys-udm1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"udm")
        if "radisys-udr1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"udr")
        if "radisys-ausf1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"ausf")

        if "radisys-amfv2-1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"amfv2")

        if "radisys-udsf1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"udsf")

        if "radisys-nrf1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"nrf")
        if "radisys-nef1" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"nef")
        if "radisys-ems" in ns:
                uninstall_nfservice(old_buildpath,old_image_version,"ems")
        if "radisys-cs1" in ns:
                uninstall_cmservice(old_buildpath,old_image_version)
        if "radisys-ps1" in ns:
                uninstall_psservice(old_buildpath,old_image_version,"ps")
        if "mongodb" in ns:
                uninstall_psservice(old_buildpath,old_image_version,"mongodb")


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

def my_function(file_load, default_nf_version, new_image_version,path):
        os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
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

def global_nffunction(file_load,path,new_image_version,cluster_ip):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
#    print(os.getcwd())
    with open (file_load, "r") as read_file:
        #read_file.preserve_quotes=True
        node = yaml.safe_load(read_file)
        check = node ["global"]["elasticHost"]
        print (check)
        read_file.close()
        return check

def global_nfelunction(file_load,path,new_image_version,cluster_ip,nf):
        os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
        fin = open(file_load, "rt")
        #read file contents to string
        data = fin.read()
        #replace all occurrences of the required string_function
        data = data.replace(nf, cluster_ip)
        fin.close()
        #open the input file in write mode
        fin = open(file_load, "wt")
        #overrite the input file with the resulting data
        fin.write(data)
        #close the file
        fin.close()

def amf_function(file_load,path,new_image_version,n2_ip):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
#    print(os.getcwd())
    with open (file_load) as read_file:
        node = yaml.safe_load(read_file)
        node["amf-n2iwf"]["amf_n2iwf"]["appConfig"]["externalIP"]= n2_ip
        print(node)
        with open(file_load, 'w') as yaml_file:
           data = yaml_file.write(yaml.dump(node, sort_keys=False, default_flow_style=False))
           file_load = data

def nef_function(file_load,path,new_image_version,nef_pp,nef_ee):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
#    print(os.getcwd())
    with open (file_load) as read_file:
        node = yaml.safe_load(read_file)
        node["nef-ee"]["nef_ee"]["appConfig"]["externalIP"]= nef_ee
        node["nef-3gpp-5glan-pp"]["nef_3gpp_5glan_pp"]["appConfig"]["externalIP"]=nef_pp
        print(node)
        with open(file_load, 'w') as yaml_file:
           data = yaml_file.write(yaml.dump(node, sort_keys=False, default_flow_style=False))
           file_load = data

def upf_pcifunction(file_load,path,new_image_version,n3_pci,n6_pci):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
#    print(os.getcwd())
    with open (file_load, "r") as read_file:
        #read_file.preserve_quotes=True
        node = yaml.safe_load(read_file)
        check = node ["upf"]["upf"]["intfConfig"]["nguInterface"]["pciAddress"]
        check_1 = node ["upf"]["upf"]["intfConfig"]["n6Interface"]["pciAddress"]
        read_file.close()
        return check, check_1





def upf_function(file_load,default_nf_version,new_image_version,sriov,path,n3_old_pci,n6_old_pci,n3_pci,n6_pci):
        os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
        fin = open(file_load, "rt")
        #read file contents to string
        data = fin.read()
        #replace all occurrences of the required string_function
        data = data.replace(default_nf_version, new_image_version)
        if sriov.casefold() == "no" or sriov.casefold() == "n":
            data = data.replace("sriov", "devPassthrough")
        data = data.replace(n3_old_pci, n3_pci)
        data = data.replace(n6_old_pci, n6_pci)
        #close the input file
        fin.close()
        #open the input file in write mode
        fin = open(file_load, "wt")
        #overrite the input file with the resulting data
        fin.write(data)
        #close the file
        fin.close()




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



######### Install nf services
def install_emsservice(path,new_image_version):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
    os.system("sh install_ems.sh")

def install_nfservice(path,new_image_version):
    os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
    time.sleep(1)
    os.system("sh install_udsf.sh")
    time.sleep(1)
    os.system("sh install_nrf.sh")
    time.sleep(1)
    os.system("sh install_nssf.sh")
    time.sleep(1)
    os.system("sh install_udm.sh")
    time.sleep(1)
    os.system("sh install_udr.sh")
    time.sleep(1)
    os.system("sh install_ausf.sh")
    time.sleep(1)
    os.system("sh install_amfv2.sh")
    time.sleep(1)
    os.system("sh install_smf.sh")
    time.sleep(1)
    os.system("sh install_upf.sh")
    time.sleep(1)
    time.sleep(1)
    ns = exec_cmd("kubectl get ns")
    print(ns)
    if "radisys-upf1" and "radisys-smf1" and "radisys-nssf1" and "radisys-udm1" and "radisys-udr1" and "radisys-ausf1" and "radisys-amfv2-1" and "radisys-udsf1" and "radisys-nrf1" and "radisys-nef1" and "radisys-ems" in ns:
        os.system("kubectl get pod -A")
        print(Fore.BLUE+"\n nf services are installed sucessfully"+'\U0001F603 \n')

    else:
        print(Fore.RED+"\n FAILED TO INSTALL NF SERVICES")
        exit()
    time.sleep(1)


## Install common services
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
def neffunc(nef):
    if nef.casefold() == "yes" or nef.casefold() == "y":
        my_function(file_load_16,default_nf_version,new_image_version,path)
        nef_function(file_load_16,path,new_image_version,nef_pp,nef_ee)
        os.chdir(path+"/TRILLIUM_5GCN_CNF_REL_"+new_image_version+"/nf-services/scripts/")
        os.system("sh install_nef.sh")
        time.sleep(1)
        ns = exec_cmd("kubectl get ns")
        print(ns)
        if "radisys-nef1" in ns:
            print(Fore.BLUE+"Nef installed sucessfully \n")

    else:
        print(Fore.BLUE+"Nef is not supported in this version")

## Install Platform services
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

#stdoutOrigin=sys.stdout
#sys.stdout = open("log.txt", "w")
date()
print(Fore.BLUE+"\n Starting uninstall procedure \n")
uninstall()
date()
print(Fore.BLUE+"\n Starting the image deletion process \n")
delete = ("crictl images | grep "+old_image_version+"| awk '{print $3}' | xargs crictl rmi")
image_delete = exec_cmd(delete)
print(image_delete)

print(Fore.BLUE+"\n Clear data from mnt folders based on user input \n")
cleardb = clear_db()
date()

date()
#print(Fore.BLUE+"\n Disk Usage and Memory allocation checks \n")
#memdisk()

#date()
print(Fore.BLUE+"\n Starting the unzip process for new package \n")
untar = ("tar -xvf TRILLIUM_5GCN_CNF_REL_"+new_image_version+".tar.gz")
exec_cmduntar(untar,path)

date()
#cluster_reset(cluster_ip,kubernetes_image_version,kubernetes_build_path,file_load_14)

date()

basepath = "cp load.sh"+" "+path
print (basepath)

#date()
print(Fore.BLUE+"\n Copying the load.sh script to base path \n")
copy_load(basepath,path)

print(Fore.BLUE+"\n Loading the new images \n")
load_fun(new_image_version,path)

date()
elastic_status(file_load_15,cluster_ip)

date()
print(Fore.BLUE+"\n Starting the Platform service installation \n")
ps_ingress(cluster_ip,file_load_10,path,new_image_version)
ps_el(cluster_ip,file_load_11,path,new_image_version)
platform_services(path,new_image_version)

date()
print(Fore.BLUE+"\n Starting the Common service installation \n")
cs_function(file_load_9,default_nf_version,new_image_version,path)
common_service(path,new_image_version)

date()
print(Fore.BLUE+"\n Starting nf config changes in respctive yaml file \n")
elastic = global_nffunction(file_load_13,path,new_image_version, cluster_ip)
global_nfelunction(file_load_13,path,new_image_version, cluster_ip,elastic)
my_function(file_load,default_nf_version,new_image_version,path)
my_function(file_load_1,default_nf_version,new_image_version,path)
my_function(file_load_2,default_nf_version,new_image_version,path)
my_function(file_load_3,default_nf_version,new_image_version,path)
my_function(file_load_4,default_nf_version,new_image_version,path)
my_function(file_load_5,default_nf_version,new_image_version,path)
my_function(file_load_6,default_nf_version,new_image_version,path)
my_function(file_load_7,default_nf_version,new_image_version,path)
my_function(file_load_12,default_nf_version,new_image_version,path)
neffunc(nef)
amf_function(file_load_7,path,new_image_version,n2_ip)
pci = upf_pcifunction(file_load_8,path,new_image_version,n3_pci,n6_pci)
n3_old_pci = pci[0]
n6_old_pci = pci[1]
print (n3_old_pci)
print (n6_old_pci)
upf_function(file_load_8,default_nf_version,new_image_version,sriov,path,n3_old_pci,n6_old_pci,n3_pci,n6_pci)
date()
print(Fore.BLUE+"\n Starting EMS installation \n")
install_emsservice(path,new_image_version)

date()
print(Fore.BLUE+" \n Please type Yes after pushing the nf config through EMS \n")
userinput = input(Fore.BLUE+"\n Do you want to continue the nf installation yes or no: ")
print(Style.RESET_ALL)
if userinput.casefold() == "yes" or userinput.casefold() == "y":
    install_nfservice(path,new_image_version)
else:
    print (Fore.RED + Back.GREEN+"User aborted the upgrade!!!!"+'\U0001F643')
    exit()
