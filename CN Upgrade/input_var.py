cluster_ip = "1.1.1.1"
## The image version want to uninstall (N build)
old_image_version = "4.2.0"
## The image version want to install (N+1)
new_image_version = "4.2.0"
### N2 IP address for gNB and AMF connection
n2_ip ="1.1.1.1"

## NEF IP address, for the release above 4.2.0
nef = "No"
nef_ee ="1.1.1.1"
nef_pp ="1.1.1.1"

### DN interface PCI
n6_pci ="0000:00:0a.0"

## Ngu interface PCI
n3_pci ="0000:00:09.0"

## Build path of the upgrade build (N+1)
path = "/home/labadmin/5GC_4.2.0_EA1"

## Build path of the N build
old_buildpath ="/home/labadmin/5GC_4.2.0_EA1"

## If Yes data will be cleared from mnt direcotry
Clear_data_from_mnt_folders = "Yes"

### if testbed is baremetal please sriov as yes
sriov = "no"
