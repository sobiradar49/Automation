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
old_image_version = input_var.old_image_version
old_buildpath = input_var.old_buildpath
nef_ee = input_var.nef_ee
nef_pp = input_var.nef_pp
#kubernetes_image_version = input_var.kubernetes_image_version
#kubernetes_build_path = input_var.kubernetes_build_path
nef = input_var.nef


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
        if nef.casefold() == "yes" or nef..casefold() == "Y":
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
date()
print(Fore.BLUE+"\n Starting uninstall procedure \n")
uninstall()
