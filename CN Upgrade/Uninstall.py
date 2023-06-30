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
