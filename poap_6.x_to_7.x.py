#
# Version : 2.0
#
#   Version  |     Author     |  Description
#   1.0            -             Initial version
#   2.0        deepagar          Refactored and added logging and traceback for errors
#
#

#md5sum="da3fd031191a799d274a324a0fda063a"
# If any changes to this script file are made, please run the below command
# in bash after modifications.
# The above is the (embedded) md5sum of this file taken without this line,
# can be # created this way if using a bash shell:
# f=poap_script.py ; cat $f | sed '/^#md5sum/d' > $f.md5 ; sed -i "s/^#md5sum=.*/#md5sum=\"$(md5sum $f.md5 | sed 's/ .*//')\"/" $f
# This way this script's integrity can be checked in case you do not trust
# tftp's ip checksum. This integrity check is done by /isan/bin/poap.bin).
# The integrity of the files downloaded later (images, config) is checked
# by downloading the corresponding file with the .md5 extension and is
# done by this script itself.
###################################################@@CVS_HEADER_BEGIN
#
#      File:  poap_script.py
#      Name:
#
#      Description:
#               Script to execute NXOS CLIs to perform copy config,
#               kickstart, isan, etc...
#
# Copyright (c) 1985-2004, 2007-2013, 2015 by cisco Systems, Inc.
# All rights reserved.
#
# $Id$
# $Source$
#
#####################################################@@CVS_HEADER_END


########################################################
#
# Best Practices
#
#
#
#  ************ POAP Common **************
# File list to keep in storage medium:
# - conf_FOC1848R2AH.cfg <- Store running config in this FOC1848R2AH is Serial number of box chasis
# - n3500-uk9-kickstart.6.0.2.XX.0.53.bin <- kickstart image
# - n3500-uk9.6.0.2.XX.0.53.bin <- system image
# - poap_script.py <- replace name of kickstart and system image in this script as of file names above
#
#
#
# # sh inventory
# NAME: "Chassis", DESCR: "Nexus 3548 Chassis"
# PID: N3K-C3548P-10GX , VID: V00 , SN: FOC1848R2AH
#
#
#
#  ************* POAP with USB *************
#
#
# 1. Set Source path of Config file
#    config_path = "/"
#
# 2. Set Transfer Protocol
#    transfer_protocol = "scp"
#
# 3. Set Source file name of System Image
#    system_image_src = "n3000-uk9.6.0.2.U1.1.bin"
#
# 4. Set Source file name of Kickstart Image
#    kickstart_image_src = "n3000-uk9-kickstart.6.0.2.U1.1.bin"
#
# 5. Set Source path of both System and Kickstart images
#    image_path = "/"
#
#
# ************* POAP with TFTP *************
#
#
# 1. Create md5 for config file using chasis serial number
#    switch# sh inventory
#    NAME: "Chassis", DESCR: "Nexus 3548 Chassis"
#    PID: N3K-C3548P-10G    , VID: V01 , SN: FOC1721R2JN
#    Create md5 files conf_FOC1721R2JN.cfg.md5 for conf_FOC1721R2JN.cfg
#    # md5sum conf_FOC1721R2JN.cfg
#      2c31208deb8b193b5ee31587abb12684  conf_FOC1721R2JN.cfg
#    # cat conf_FOC1721R2JN.cfg.md5
#      md5 = 2c31208deb8b193b5ee31587abb12684
#
# 2. Create md5 file for kickstart image
#    Create md5 file n3000-uk9-kickstart.6.0.2.U1.1.bin.md5 for n3000-uk9-kickstart.6.0.2.U1.1.bin
#    # md5sum n3000-uk9-kickstart.6.0.2.U1.1.bin
#      09d0d0df61291e3d8410ecc8bcdda18e  n3000-uk9-kickstart.6.0.2.U1.1.bin
#    # cat n3000-uk9-kickstart.6.0.2.U1.1.bin.md5
#      md5 = 09d0d0df61291e3d8410ecc8bcdda18e
#
# 3. Create md5 file for system image
#    Create md5 files n3000-uk9.6.0.2.U1.1.bin.md5 for n3000-uk9.6.0.2.U1.1.bin
#    # md5sum n3000-uk9.6.0.2.U1.1.bin
#      6e8498f9433c4500e469a19e64b7bca n3000-uk9.6.0.2.U1.1.bin
#    # cat n3000-uk9.6.0.2.U1.1.bin.md5
#      md5 = 6e8498f9433c4500e469a19e64b7bca
#
# 4. Set Source path of Config file (say in /tftpboot/)
#    config_path = "/"
#
# 5. Set Transfer Protocol
#    transfer_protocol = "tftp"
#
# 6. Set Source file name of System Image
#    system_image_src = "n3000-uk9.6.0.2.U1.1.bin"
#
# 7. Set Source file name of Kickstart Image
#    kickstart_image_src = "n3000-uk9-kickstart.6.0.2.U1.1.bin"
#
# 8. Set Source path of both System and Kickstart images (say in /tftpboot/)
#    image_path = "/"
#
# 9. Set DHCP  Server username
#	 username = "username"
#
# 10. Set DHCP Server password
#    password = "password"
#
# 11. Set DHCP Server hostname
#    hostname = "192.168.1.1"
#
# 12. Set md5 for POAP script
#     f=poap_script.py ; cat $f | sed '/^#md5sum/d' > $f.md5 ; sed -i "s/^#md5sum=.*/#md5sum=\"$(md5sum $f.md5 | sed 's/ .*//')\"/" $f
#
#
# ************* POAP with FTP *************
#
# 1. Create md5 for config file using chasis serial number
#    switch# sh inventory
#    NAME: "Chassis", DESCR: "Nexus 3548 Chassis"
#    PID: N3K-C3548P-10G    , VID: V01 , SN: FOC1721R2JN
#    Create md5 files conf_FOC1721R2JN.cfg.md5 for conf_FOC1721R2JN.cfg
#    # md5sum conf_FOC1721R2JN.cfg
#      2c31208deb8b193b5ee31587abb12684  conf_FOC1721R2JN.cfg
#    # cat conf_FOC1721R2JN.cfg.md5
#      md5 = 2c31208deb8b193b5ee31587abb12684
#
# 2. Create md5 file for kickstart image
#    Create md5 files n3000-uk9-kickstart.6.0.2.U1.1.bin.md5 for n3000-uk9-kickstart.6.0.2.U1.1.bin
#    # md5sum n3000-uk9-kickstart.6.0.2.U1.1.bin
#      09d0d0df61291e3d8410ecc8bcdda18e  n3000-uk9-kickstart.6.0.2.U1.1.bin
#    # cat n3000-uk9-kickstart.6.0.2.U1.1.bin.md5
#      md5 = 09d0d0df61291e3d8410ecc8bcdda18e
#
# 3. Create md5 file for system image
#    Create md5 files n3000-uk9.6.0.2.U1.1.bin.md5 for n3000-uk9.6.0.2.U1.1.bin
#    # md5sum n3000-uk9.6.0.2.U1.1.bin
#      6e8498f9433c4500e469a19e64b7bca n3000-uk9.6.0.2.U1.1.bin
#    # cat n3000-uk9.6.0.2.U1.1.bin.md5
#      md5 = 6e8498f9433c4500e469a19e64b7bca
#
# 4. Set Source path of Config file (say in /tftpboot/)
#    config_path = "/tftpboot/"
#
# 5. Set Transfer Protocol
#    transfer_protocol = "ftp"
#
# 6. Set Source file name of System Image
#    system_image_src = "n3000-uk9.6.0.2.U1.1.bin"
#
# 7. Set Source file name of Kickstart Image
#    kickstart_image_src = "n3000-uk9-kickstart.6.0.2.U1.1.bin"
#
# 8. Set Source path of both System and Kickstart images (say in /tftpboot/)
#    image_path = "/tftpboot/"
#
# 9. Set DHCP Server username
#	 username = "username"
#
# 10. Set DHCP Server password
#    password = "password"
#
# 11. Set DHCP Server hostname
#    hostname = "192.168.1.1"
#
# 12. Set md5 for POAP script
#     f=poap_script.py ; cat $f | sed '/^#md5sum/d' > $f.md5 ; sed -i "s/^#md5sum=.*/#md5sum=\"$(md5sum $f.md5 | sed 's/ .*//')\"/" $f
#
########################################################

#script execution timeout value should be in seconds
#script_timeout=1200

from cisco import cli
from cisco import transfer
from time import gmtime, strftime
from cisco import md5sum
import signal
import os
import string
import commands
import shutil
import glob
import syslog
import time
import traceback
import re

# Host name and user credentials
username = "root"
password = "nbv12345\r"
hostname = "10.197.121.180"
vrf	 = os.environ['POAP_VRF'] 

# POAP can use 3 modes to obtain the config file.
# - 'poap_static' - file is statically specified
# - 'poap_location' - CDP neighbor of interface on which DHCPDISCOVER arrived
#                     is used to derive the config file
# - 'poap_serial_number' - switch serial number is used to derive the config file
# - 'poap_mac' - use the interface (mgmt 0 interface / Single MAC address for all the
#        front-panel interface) MAC address to derive the configuration filename
#        (Example: for MAC Address 00:11:22:AA:BB:CC" the default configuration
#        file looked for would be conf_001122AABBCC.cfg
# - 'poap_hostname' - Use the hostname from the DHCP OFFER to derive the configuration
# 	file name (Example: conf_N3K-Switch-1.cfg for hostname 'N3K-Switch-1'

########################################################

poap_config_file_mode = "poap_serial_number"

# Required space to copy config kickstart and system image in KB
required_space = 300000

# Source path of Config file
config_path = "/tftpboot/"

# Source path of both System and Kickstart images
image_path = "/tftpboot/"

# Transfer Protocol
transfer_protocol = "scp"

# Source file name of System Image
system_image_src = "nxos.7.0.3.I2.3.6.bin"

# Source file name of Kickstart Image
kickstart_image_src = "n3000-uk9-kickstart.6.0.2.U1.1.bin"

single_image_poap_flag = 0

####### Config File Infos #######

# Source file name of Config file
config_file_src = "poap.cfg"

# Temperory Destination file of Config file
config_file_dst = "poap_replay.cfg"

# indicates whether config file is copied
config_copied = 0

# Destination file name for those lines in config which starts with system vlan, interface breakout, hardware profile portmode or hardware profile tcam
config_file_dst_first = "poap_1.cfg"

# Desination file name for those lines in config which does not match above criterea.
config_file_dst_second = "poap_2.cfg"

# indicates whether first config file is empty or not
emptyFirstFile = 1

# Destination Path
destination_path = "/bootflash/"


####### System and Kickstart image info #######

# Destination file name of System Image
system_image_dst = "n3k.s"

# in-use file name of System Image *** DON'T EDIT ***
system_image_saved = ""

# indicates if System Image is copied
system_image_copied = 0

# Destination file name of Kickstart Image
kickstart_image_dst = "n3k.k"

# in-use file name of Kickstart Image *** DON'T EDIT ***
kickstart_image_saved = ""

# indicates if Kickstart Image is copied
kickstart_image_copied = 0

# Timeout info
config_timeout = 120
system_timeout = 2100
kickstart_timeout = 900

# USB slot info. By default its USB slot 1, if not specified specifically.
# collina2 has 2 usb ports. To enable poap in usb slot 2 user has to set the
# value of usbslot to 2.
usbslot = 1

# Log File name
try:
    if os.environ['POAP_PHASE'] == "USB":
        poap_script_log = "/bootflash/%s_poap_%s_usb_script.log" % (strftime("%Y%m%d%H%M%S", gmtime()), os.environ['POAP_PID'])
    else:
        poap_script_log = "/bootflash/%s_poap_%s_script.log" % (strftime("%Y%m%d%H%M%S", gmtime()), os.environ['POAP_PID'])
except Exception as inst:
    print (inst)

#String2Mac Conversion
def Str2Mac (poap_syslog_mac = ""):
	poap_syslog_mac = "%s:%s:%s:%s:%s:%s" % (poap_syslog_mac[0:2], poap_syslog_mac[2:4], poap_syslog_mac[4:6], poap_syslog_mac[6:8], poap_syslog_mac[8:10], poap_syslog_mac[10:12])
	return poap_syslog_mac


# Syslog Prefix
def setSyslogPrefix():
    try:
        global poap_syslog_prefix, env, poap_syslog_mac
        if os.environ.has_key('POAP_SERIAL'):
            poap_syslog_prefix = "S/N[%s]" % os.environ['POAP_SERIAL']
        if os.environ['POAP_PHASE'] == "USB":
            if os.environ.has_key('POAP_RMAC'):
                poap_syslog_mac = "%s" % os.environ['POAP_RMAC']
                poap_syslog_prefix = "%s-MAC[%s]" % (poap_syslog_prefix, poap_syslog_mac)
                return
            if os.environ.has_key('POAP_MGMT_MAC'):
                poap_syslog_mac = "%s" % os.environ['POAP_MGMT_MAC']
                poap_syslog_prefix = "%s-MAC[%s]" % (poap_syslog_prefix, poap_syslog_mac)
                return
        else:
            if os.environ.has_key('POAP_MAC'):
                poap_syslog_mac = "%s" % os.environ['POAP_MAC']
                poap_syslog_mac = Str2Mac (poap_syslog_mac)
                poap_syslog_prefix = "%s-MAC[%s]" % (poap_syslog_prefix, poap_syslog_mac)
                return
    except Exception as inst:
        poap_log(poap_script_log_handler, "Set syslog prefix Failed : %s" % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)


# Log file handler
poap_script_log_handler = open(poap_script_log, "w+")

setSyslogPrefix()

def poap_cleanup_script_logs() :
    try:
        preserve_last_logs = 4
        files = []

        path = destination_path

        for infile in glob.glob( os.path.join(path, '*poap*script.log')):
            files.append(infile)
        files.sort()
        files.reverse()

        count = 0
        for file in files:
            count = count + 1
            if count > preserve_last_logs:
                os.remove(file)
    except Exception as inst:
        poap_log(poap_script_log_handler, "Poap cleanup script logs failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

def poap_log (file_descriptor, info):
    global poap_syslog_prefix
    info = "%s - %s" % (poap_syslog_prefix, info)
    syslog.syslog(9, info)
    file_descriptor.write("\n")
    file_descriptor.write(info)
    file_descriptor.flush()

def remove_file (filename) :
    try:
        os.remove(filename)
    except os.error:
        poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
        pass

def cleanup_files () :
    poap_log(poap_script_log_handler, "Cleanup files")
    global config_file_dst, config_file_dst_first, config_file_dst_second, system_image_dst, kickstart_image_dst, poap_script_log_handler
    poap_log(poap_script_log_handler, "INFO: delete all files")
    if config_copied == 1:
        remove_file("/bootflash/%s" % config_file_dst)
    remove_file("/bootflash/%s" % config_file_dst_first)
    remove_file("/bootflash/%s" % config_file_dst_second)
    if system_image_copied == 1:
    	remove_file("/bootflash/%s" % system_image_dst)
    if kickstart_image_copied == 1:
    	remove_file("/bootflash/%s" % kickstart_image_dst)
    remove_file("/bootflash/%s.tmp" % config_file_dst)
    remove_file("/bootflash/%s.tmp" % system_image_dst)
    remove_file("/bootflash/%s.tmp" % kickstart_image_dst)
    remove_file("/bootflash/%s" % config_file_dst)
    remove_file("/bootflash/%s" % system_image_dst)
    remove_file("/bootflash/%s" % kickstart_image_dst)


def sig_handler_no_exit (signum, frame) :
    global poap_script_log_handler
    poap_log(poap_script_log_handler, "INFO: SIGTERM Handler while configuring boot variables")


def sigterm_handler (signum, frame):
    try:
        global poap_script_log_handler
        poap_log(poap_script_log_handler, "INFO: SIGTERM Handler")
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)
    except Exception as inst:
        poap_log(poap_script_log_handler, "Sigterm handler Failed : %s" % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

def removeFile (filename) :
    try:
    	os.remove(filename)
    except:
        poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
        pass

signal.signal(signal.SIGTERM, sigterm_handler)

# Procedure to split config file using global information
def splitConfigFile ():
    try:
        poap_log(poap_script_log_handler, "Split Config file")
        global config_file_dst, config_file_dst_first, config_file_dst_second, emptyFirstFile, poap_script_log_handler, single_image_poap_flag, system_image_dst
        configFile = open("/bootflash/%s" % config_file_dst, "r")
        configFile_first = open("/bootflash/%s" % config_file_dst_first, "w+")
        configFile_second = open("/bootflash/%s" % config_file_dst_second, "w+")
        line = configFile.readline()
        while line != "":
			if not string.find(line, "system vlan", 0, 11) or not string.find(line, "interface breakout", 0, 18) or not string.find(line, "hardware profile portmode", 0, 25) or not string.find(line, "hardware profile forwarding-mode warp", 0, 37)  or not string.find(line, "hardware profile tcam", 0, 21) or not string.find(line, "type fc", 0, 7) or not string.find(line, "fabric-mode 40G", 0, 15) or not string.find(line, "system urpf" , 0, 11) or not string.find(line, "hardware profile ipv6", 0, 21) or not string.find(line, "system routing", 0, 14) or not string.find(line, "hardware profile multicast service-reflect", 0, 43) or not string.find(line, "ip service-reflect mode", 0, 24) or not string.find(line, "udf", 0, 3) :
				configFile_first.write(line)
			        if emptyFirstFile is 1:
                                    poap_log(poap_script_log_handler,"setting empty file to 0 for line %s" % line)
				    emptyFirstFile = 0
			else:
				configFile_second.write(line)
			line = configFile.readline()

        # for poap across images set boot varible in the first config file 
        poap_log(poap_script_log_handler, "value of empty file is %d " % emptyFirstFile)
        if single_image_poap_flag is 1:
           if emptyFirstFile is 0 :
              cmd = "boot nxos bootflash:/%s" % system_image_dst 
              poap_log(poap_script_log_handler,"writing boot command: %s to first config file" % cmd)
              configFile_first.write("%s\n" % cmd) 
           else :
              cmd = "boot nxos bootflash:/%s" % system_image_dst
              poap_log(poap_script_log_handler,"writing boot command: %s to second config file" % cmd)
              configFile_second.write("%s\n" % cmd)

        configFile.close()
        removeFile("/bootflash/%s" % config_file_dst)
        configFile_first.close()
        if emptyFirstFile is 1:
			removeFile("/bootflash/%s" % config_file_dst_first)

        configFile_second.close()

    except Exception as inst:
        poap_log(poap_script_log_handler, "Split Config File Failed : %s" % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

def verifyMD5sumofFile (md5given, filename):
    try:
        poap_log(poap_script_log_handler, "Verifying MD5 checksum")

        if not os.path.exists("%s" % filename):
            poap_log(poap_script_log_handler, "Warning: File %s does not exit" % filename)
            poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
            return False

        md5calculated = md5sum(filename, 0)

        poap_log(poap_script_log_handler, "Verifying MD5 checksum md5given = %s md5calculated = %s" % (md5given, md5calculated))

        if md5given == md5calculated:
            poap_log(poap_script_log_handler, "MD5 match filename = %s md5given = %s md5calculated = %s" % (filename, md5given, md5calculated))
            return True

        poap_log(poap_script_log_handler, "MD5 mis-match filename = %s md5given = %s md5calculated = %s" % (filename, md5given, md5calculated))
        poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
        return False
    except Exception as inst:
        poap_log(poap_script_log_handler, "Verify MD5 Sum Failed - %s : for %s " % (inst, filename))
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

def getMD5SumGiven (keyword, filename) :
    try:
        file = open("/bootflash/%s" % filename, "r")
        line = file.readline()
        while line != "":
            if not string.find(line, keyword, 0, len(keyword)) :
                line = line.split("=")
                line = line[1]
                line = line.strip()
                file.close()
                return line
            line = file.readline()
        file.close()

    except Exception as inst:
        poap_log(poap_script_log_handler, "Get MD5 Sum Failed - %s : from /bootflash/%s" % (inst, filename))
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

    return ""

def doCopyWithoutExit (protocol = "", host = "", source = "", dest = "", vrf = "management", login_timeout=10, user = "", password = "", dest_tmp = ""):
    try:
        poap_log(poap_script_log_handler, "Copying file transfer_protocol=%s hostname=%s source=%s destination=%s vrf=%s login_timeout=%s username=%s destination_tmp=%s" % (protocol, host, source, dest, vrf, login_timeout, user, dest_tmp))
        global usbslot

        if os.path.exists("/bootflash/%s" % dest_tmp):
            os.remove("/bootflash/%s" % dest_tmp)

        if os.environ['POAP_PHASE'] == "USB":
            try:
                if usbslot is 2:
                    copy_src = "/usbslot2/%s" % (source)
                else:
                    copy_src = "/usbslot1/%s" % (source)

                copy_dst = "/bootflash/%s" % (dest_tmp)
                if os.path.exists(copy_src):
                    poap_log(poap_script_log_handler, " Copying from %s to %s" % (copy_src, copy_dst))
                    shutil.copy (copy_src, copy_dst)
                else:
                    poap_log(poap_script_log_handler, "Warning: File %s does not exit" % copy_src)
                    poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                    return False
            except Exception as inst:
                poap_log(poap_script_log_handler, "Copy Failed: %s copy_src = %s to copy_dst = %s" % (inst, copy_src, copy_dst))
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                cleanup_files()
                poap_script_log_handler.close()
                exit(1)
        else:
            try:
                poap_log(poap_script_log_handler, " Transfering using %s from %s to %s" % (protocol, source, dest_tmp))
                transfer(protocol, host, source, dest_tmp, vrf, login_timeout, user, password)
            except Exception as inst:
                poap_log(poap_script_log_handler, "Copy Failed: %s protocol = %s host = %s source = %s to dest_tmp = %s vrf = %s login_timeout = %s" % (inst, protocol, host, source, dest_tmp, vrf, login_timeout))
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                cleanup_files()
                poap_script_log_handler.close()
                exit(1)

        try:
            dest_tmp = "%s%s" % (destination_path, dest_tmp)
            dest	 = "%s%s" % (destination_path, dest)
        except Exception as inst:
            poap_log(poap_script_log_handler, "Do Copy Without Exit Failed - %s" % inst)
            poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
            cleanup_files()
            poap_script_log_handler.close()
            exit(1)

        try:
            os.rename(dest_tmp, dest)
        except Exception as inst:
            poap_log(poap_script_log_handler, "Rename Failed - %s : for dest_tmp %s to dest = %s" % (inst, dest_tmp, dest))
            poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
            cleanup_files()
            poap_script_log_handler.close()
            exit(1)

    except Exception as inst:
        poap_log(poap_script_log_handler, "Do Copy Without Exit Failed - %s : from /bootflash/%s" % (inst, filename))
        poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

    return True

def doCopy (protocol = "", host = "", source = "", dest = "", vrf = "management", login_timeout=10, user = "", password = "", dest_tmp = ""):
    try:
        poap_log(poap_script_log_handler, "Copying file transfer_protocol=%s hostname=%s source=%s destination=%s vrf=%s login_timeout=%s username=%s destination_tmp=%s" % (protocol, host, source, dest, vrf, login_timeout, user, dest_tmp))
        global usbslot
        if os.path.exists("/bootflash/%s" % dest_tmp):
            os.remove("/bootflash/%s" % dest_tmp)

        if os.environ['POAP_PHASE'] == "USB":
            if usbslot is 2:
                copy_src = "/usbslot2/%s" % (source)
            else:
                copy_src = "/usbslot1/%s" % (source)

            copy_dst = "/bootflash/%s" % (dest_tmp)
            if os.path.exists(copy_src):
                poap_log(poap_script_log_handler, "/usbslot%d/%s exists" % (usbslot, source))
                poap_log(poap_script_log_handler, " Copying from %s to %s" % (copy_src, copy_dst))
                shutil.copy (copy_src, copy_dst)
            else:
                poap_log(poap_script_log_handler, "/usbslot%d/%s NOT exists" % (usbslot, source))
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                cleanup_files()
                poap_script_log_handler.close()
                exit(1)
        else:
            poap_log(poap_script_log_handler, " Transfering using %s from %s to %s" % (protocol, source, dest_tmp))
            transfer(protocol, host, source, dest_tmp, vrf, login_timeout, user, password)
    except Exception as inst1:
        poap_log(poap_script_log_handler, "Copy Failed: %s copy_src=%s to copy_dst=%s" % (inst1, copy_src, copy_dst))
        poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

    try:
        dest_tmp = "%s%s" % (destination_path, dest_tmp)
        dest	 = "%s%s" % (destination_path, dest)
    except Exception as inst2:
        poap_log(poap_script_log_handler, "Do Copy Failed : %s" % inst2)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

    try:
        os.rename(dest_tmp, dest)
    except Exception as inst3:
        poap_log(poap_script_log_handler, "Rename Failed - %s : for dest_tmp %s to dest = %s" % (inst3, dest_tmp, dest))
        poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

def copyMd5Info (file_path, file_name):
    try:
        poap_log(poap_script_log_handler, "Copying MD5 information")
        global username, hostname, poap_script_log_handler, password
        md5_file_name = "%s.md5" % file_name
        if os.path.exists("/bootflash/%s" % md5_file_name):
            removeFile("/bootflash/%s" % md5_file_name)

        tmp_file = "%s.tmp" % md5_file_name
        time = config_timeout
        src = "%s%s" % (file_path, md5_file_name)
    	poap_log(poap_script_log_handler, "INFO: Starting Copy of MD5 File transfer_protocol = %s src = %s dest =  /bootflash/%s" % (transfer_protocol, src, md5_file_name))
        return doCopyWithoutExit (transfer_protocol, hostname, src, md5_file_name, vrf, time, username, password, tmp_file)
    except Exception as inst:
        poap_log(poap_script_log_handler, "Copy Md5 Info Failed : %s" % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

    return False

# Procedure to extract kickstart and system images from "show boot"
def extractBootVar ():
    try:
        poap_log(poap_script_log_handler, "Extract kickstart and system images from \"show boot\"")
        global system_image_saved, kickstart_image_saved
        poap_log(poap_script_log_handler, "show boot")
        bootOutput = cli ("show boot")
        bootOutArray = bootOutput[1].split("\n")
        bootRaw = bootOutArray[3].split('=')
        if len(bootRaw) == 2:
            bootlist = bootRaw[1].split(':')
            kickstart_image_saved = bootlist[1]
        bootRaw = bootOutArray[4].split('=')
        if len(bootRaw) == 2:
        	bootlist = bootRaw[1].split(':')
        	system_image_saved = bootlist[1]
        poap_log(poap_script_log_handler, "Boot variables: kickstart:%s, system:%s" % (kickstart_image_saved, system_image_saved))
        return
    except Exception as inst:
        poap_log(poap_script_log_handler, "Extract bootvar failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

# Procedure to copy config file using global information
def copyConfig ():
    try:
        poap_log(poap_script_log_handler, "Copying config file")
        global username, hostname, config_path, config_file_src, config_file_dst, config_timeout, poap_script_log_handler, emptyFirstFile, password
        org_file = config_file_dst
        md5sumGiven = ""
        if copyMd5Info(config_path, config_file_src):
            md5sumGiven = getMD5SumGiven("md5sum", "%s.md5" % config_file_src)
            removeFile("/bootflash/%s.md5" % config_file_src)
            if md5sumGiven and os.path.exists("/bootflash/%s" % org_file):
                if verifyMD5sumofFile(md5sumGiven, "/bootflash/%s" % org_file):
                    poap_log(poap_script_log_handler, "INFO: File /bootflash/%s already exists:Config filename & MD5 match" % org_file)
                    config_copied = 1
                    splitConfigFile()
                    return;
        else:
            if os.path.exists("/bootflash/%s" % org_file):
                poap_log(poap_script_log_handler, "INFO: File /bootflash/%s already exists" % org_file)
                config_copied = 1
                splitConfigFile()
                return;
        poap_log(poap_script_log_handler, "INFO: Starting Copy of Config File to /bootflash/%s" % org_file)
        tmp_file = "%s.tmp" % org_file
        time = config_timeout
        src = "%s%s" % (config_path, config_file_src)

        doCopy (transfer_protocol, hostname, src, org_file, vrf, time, username, password, tmp_file)
        config_copied = 1
        if md5sumGiven:
            if not verifyMD5sumofFile(md5sumGiven, "%s%s" % (destination_path, org_file)):
                poap_log(poap_script_log_handler, "#### config file %s%s MD5 verification failed #####\n" % (destination_path, org_file))
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                cleanup_files()
                poap_script_log_handler.close()
                exit(1)
        splitConfigFile()
        poap_log(poap_script_log_handler, "INFO: Completed Copy of Config File to /bootflash/%s" % org_file)

    except Exception as inst:
        poap_log(poap_script_log_handler, "Copy config failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

# Procedure to copy system image using global information
def copySystem ():
    try:
        poap_log(poap_script_log_handler, "Copying system image")
        global username, hostname, image_path, system_image_src, system_image_dst, system_timeout, poap_script_log_handler, password, system_image_saved
        poap_log(poap_script_log_handler, "INFO: Starting Copy of System Image")
        org_file = system_image_dst
        md5sumGiven = ""
        if copyMd5Info(image_path, system_image_src):
            md5sumGiven = getMD5SumGiven("md5sum", "%s.md5" % system_image_src)
            removeFile("/bootflash/%s.md5" % system_image_src)
            if md5sumGiven and os.path.exists("/bootflash/%s" % org_file):
                if verifyMD5sumofFile(md5sumGiven, "/bootflash/%s" % org_file):
                    poap_log(poap_script_log_handler, "INFO: File /bootflash/%s already exists:Image Name & MD5 match" % org_file)
                    return;
            if md5sumGiven and system_image_saved:
                if verifyMD5sumofFile(md5sumGiven, "/bootflash/%s" % system_image_saved):
                    poap_log(poap_script_log_handler, "INFO: File /bootflash/%s already exists:MD5 match" % system_image_saved)
                    system_image_dst = "bootflash:%s" % system_image_saved
                    return;
        else:
            if os.path.exists("/bootflash/%s" % org_file):
                poap_log(poap_script_log_handler, "INFO: File /bootflash/%s already exists" % org_file)
                return;

        tmp_file = "%s.tmp" % org_file
        time = system_timeout
        src = "%s%s" % (image_path, system_image_src)
        doCopy (transfer_protocol, hostname, src, org_file, vrf, time, username, password, tmp_file)
        system_image_copied = 1
        if md5sumGiven:
            if not verifyMD5sumofFile(md5sumGiven, "%s%s" % (destination_path, org_file)):
                poap_log(poap_script_log_handler, "#### System file %s%s MD5 verification failed #####\n" % (destination_path, org_file))
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                poap_script_log_handler.close()
                cleanup_files()
                exit(1)
        poap_log(poap_script_log_handler, "INFO: Completed Copy of System Image to %s%s" % (destination_path, org_file))
    except Exception as inst:
        poap_log(poap_script_log_handler, "Copy system failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

# Procedure to copy kickstart image using global information
def copyKickstart ():
    try:
        poap_log(poap_script_log_handler, "Copying kickstart image")
        global username, hostname, image_path, kickstart_image_src, kickstart_image_dst, kickstart_timeout, poap_script_log_handler, password, kickstart_image_saved
        poap_log(poap_script_log_handler, "INFO: Starting Copy of Kickstart Image")
        org_file = kickstart_image_dst
        md5sumGiven = ""
        if copyMd5Info(image_path, kickstart_image_src):
            md5sumGiven = getMD5SumGiven("md5sum", "%s.md5" % kickstart_image_src)
            removeFile("/bootflash/%s.md5" % kickstart_image_src)
            if md5sumGiven and os.path.exists("/bootflash/%s" % org_file):
                if verifyMD5sumofFile(md5sumGiven, "/bootflash/%s" % org_file):
                    poap_log(poap_script_log_handler, "INFO: File %s%s already exists:Image Name & MD5 match" % (destination_path, org_file))
                    return;
            if md5sumGiven and kickstart_image_saved:
                if verifyMD5sumofFile(md5sumGiven, "/bootflash/%s" % kickstart_image_saved):
                    poap_log(poap_script_log_handler, "INFO: File %s%s already exists:MD5 match" % (destination_path, kickstart_image_saved))
                    kickstart_image_dst = "bootflash:%s" % kickstart_image_saved
                    return;
        else:
            if os.path.exists("/bootflash/%s" % org_file):
                poap_log(poap_script_log_handler, "INFO: File %s%s already exists" % (destination_path, org_file))
                return

        tmp_file = "%s.tmp" % org_file
        time = kickstart_timeout
        src = "%s%s" % (image_path, kickstart_image_src)
        doCopy (transfer_protocol, hostname, src, org_file, vrf, time, username, password, tmp_file)
        kickstart_image_copied = 1
        if md5sumGiven:
            if not verifyMD5sumofFile(md5sumGiven, "%s%s" % (destination_path, org_file)):
                poap_log(poap_script_log_handler, "#### Kickstart file %s%s MD5 verification failed #####\n" % (destination_path, org_file))
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                poap_script_log_handler.close()
                cleanup_files()
                exit(1)

        poap_log(poap_script_log_handler, "INFO: Completed Copy of Kickstart Image to %s%s" % (destination_path, org_file))

    except Exception as inst:
        poap_log(poap_script_log_handler, "Copy kickstart failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)


# Procedure to install system image
def installImages_7_x ():
    # Check ifbios upgrade is needed
    poap_log(poap_script_log_handler, "Checking if bios upgrade is needed")
    if(is_bios_upgrade_needed()):
       poap_log(poap_script_log_handler, "##############Installing new BIOS(will take upto 5 minutes dont abort)S############")
       install_bios()

    try:
        poap_log(poap_script_log_handler, "Installing system image")
        global system_image_dst, poap_script_log_handler
        timeout = -1

        try:
            cli ("config terminal ; boot nxos %s" % system_image_dst)
        except SyntaxError:
            poap_log(poap_script_log_handler, "WARNING: set boot variable system failed")
            poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
            cleanup_files()
            poap_script_log_handler.close()
            exit(1)

        command_successful = False
        timeout = 10 # minutes
        first_time = time.time()
        endtime = first_time + timeout  * 60 #sec per min
        retry_delay  = 30 # seconds
        while not command_successful:
            new_time = time.time()
            try:
                cli ("copy running-config startup-config")
                command_successful = True
            except SyntaxError:
                poap_log(poap_script_log_handler, "WARNING: copy run to start failed")
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                if  new_time  > endtime:
                    poap_log(poap_script_log_handler, "ERROR: time out waiting for  \"copy run start\" to complete successfully")
                    sys.exit(-1)
                poap_log(poap_script_log_handler, "WARNING: retry in 30 seconds")
                time.sleep( retry_delay )

        poap_log(poap_script_log_handler, "INFO: Configuration successful")

    except Exception as inst:
        poap_log(poap_script_log_handler, "Install images failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)
# Procedure to install both kickstart and system images
def installImages ():
    try:
        poap_log(poap_script_log_handler, "Installing kickstart and system images")
        global kickstart_image_dst, system_image_dst, poap_script_log_handler
        timeout = -1
        poap_log(poap_script_log_handler, "######### Copying the boot variables ##########")
        try:
            cli ("config terminal ; boot kickstart %s" % kickstart_image_dst)
        except SyntaxError:
            poap_log(poap_script_log_handler, "WARNING: set boot variable kickstart failed")
            poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
            cleanup_files()
            poap_script_log_handler.close()
            exit(1)

        try:
            cli ("config terminal ; boot system %s" % system_image_dst)
        except SyntaxError:
            poap_log(poap_script_log_handler, "WARNING: set boot variable system failed")
            poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
            cleanup_files()
            poap_script_log_handler.close()
            exit(1)

        command_successful = False
        timeout = 10 # minutes
        first_time = time.time()
        endtime = first_time + timeout  * 60 #sec per min
        retry_delay  = 30 # seconds
        while not command_successful:
            new_time = time.time()
            try:
                cli ("copy running-config startup-config")
                command_successful = True
            except SyntaxError:
                poap_log(poap_script_log_handler, "WARNING: copy run to start failed")
                poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
                if  new_time  > endtime:
                    poap_log(poap_script_log_handler, "ERROR: time out waiting for  \"copy run start\" to complete successfully")
                    sys.exit(-1)
                poap_log(poap_script_log_handler, "WARNING: retry in 30 seconds")
                time.sleep( retry_delay )

        poap_log(poap_script_log_handler, "INFO: Configuration successful")

    except Exception as inst:
        poap_log(poap_script_log_handler, "Install images failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

# Verify if free space is available to download config, kickstart and system
# images
def verifyfreespace ():
    try:
        poap_log(poap_script_log_handler, "Verifying freespace to download config, kickstart and system")
        global poap_script_log_handler, required_space
        s = os.statvfs("/bootflash/")
        freespace = (s.f_bavail * s.f_frsize) / 1024
        poap_log(poap_script_log_handler, "####The free space is %s##"  % freespace )

        if required_space > freespace:
            poap_log(poap_script_log_handler, "#### No enough space to copy the config, kickstart image and system image#####\n")
            poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
            poap_script_log_handler.close()
            exit(1)
    except Exception as inst:
        poap_log(poap_script_log_handler, "Verify free space failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)


# Procedure to set config_file based on switch serial number
def setSrcCfgFileNameSerial ():
    try:
        poap_log(poap_script_log_handler, "Setting source cfg filename based-on serial number")
        global config_file_src, poap_script_log_handler
        if os.environ.has_key('POAP_SERIAL'):
            poap_log(poap_script_log_handler, "serial number %s" % os.environ['POAP_SERIAL'])
            config_file_src = "conf_%s.cfg" % os.environ['POAP_SERIAL']

        poap_log(poap_script_log_handler, "Selected conf file name : %s" % config_file_src)
    except Exception as inst:
        poap_log(poap_script_log_handler, "Set src config filename serial failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

# Procedure to set config_file based on the interface MAC
def setSrcCfgFileNameMAC():
    try:
        poap_log(poap_script_log_handler, "Setting source cfg filename based on the interface MAC")
        global config_file_src, poap_script_log_handler, usbslot
        if os.environ['POAP_PHASE'] == "USB":

            if usbslot is 2:
                poap_log(poap_script_log_handler, "usb slot is 2")
            else:
                usbslot = 1

            config_file = "conf_%s.cfg" % os.environ['POAP_RMAC']
            poap_log(poap_script_log_handler, "Router MAC conf file name : %s" % config_file)
            if os.path.exists("/usbslot%d/%s" % (usbslot,config_file)):
                config_file_src = config_file
                poap_log(poap_script_log_handler, "Selected conf file name : %s" % config_file_src)
                return
            config_file = "conf_%s.cfg" % os.environ['POAP_MGMT_MAC']
            poap_log(poap_script_log_handler, "MGMT MAC conf file name : %s" % config_file)
            if os.path.exists("/usbslot%d/%s" % (usbslot,config_file)):
                config_file_src = config_file
                poap_log(poap_script_log_handler, "Selected conf file name : %s" % config_file_src)
                return
        else:
            if os.environ.has_key('POAP_MAC'):
                poap_log(poap_script_log_handler, "Interface MAC %s" % os.environ['POAP_MAC'])
            config_file_src = "conf_%s.cfg" % os.environ['POAP_MAC']
        poap_log(poap_script_log_handler, "Selected conf file name : %s" % config_file_src)

    except Exception as inst:
        poap_log(poap_script_log_handler, "Set src config filename mac failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

# Procedure to set config_file based on switch host name
def setSrcCfgFileNameHostName ():
    try:
        poap_log(poap_script_log_handler, "Setting source cfg filename based on switch hostname")
        global config_file_src, poap_script_log_handler
        if os.environ.has_key('POAP_HOST_NAME'):
            poap_log(poap_script_log_handler, "Host Name: [%s]" % os.environ['POAP_HOST_NAME'])
            config_file_src = "conf_%s.cfg" % os.environ['POAP_HOST_NAME']
        else:
            poap_log(poap_script_log_handler, "Host Name information missing, falling back to static mode\n")

        poap_log(poap_script_log_handler, "Selected conf file name : %s" % config_file_src)
    except Exception as inst:
        poap_log(poap_script_log_handler, "Set src config filename hostname failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

# Procedure to set config_file_src
def setSrcCfgFileNameLocation():
    try:
        poap_log(poap_script_log_handler, "Setting source cfg filename")
        global config_file_src, poap_script_log_handler, env
        startAppend = 0
        timeout = -1
        poap_log(poap_script_log_handler, "show cdp neighbors interface %s" % os.environ['POAP_INTF'])
        cdpOutput = cli ("show cdp neighbors interface %s" % os.environ['POAP_INTF'])
        cdpOutArray = cdpOutput[1].split("\n")
        cdpRaw = cdpOutArray[7].split()
        cdpRawIntf = cdpOutArray[len(cdpOutArray) - 2].split()
        cdplist = cdpRaw[0].split('(')
        switchName = cdplist[0]
        intfName   = cdpRawIntf[len(cdpRawIntf) - 1]
        config_file_src = "conf_%s_%s.cfg" % (switchName, intfName)
        config_file_src = string.replace(config_file_src, "/", "_")
        poap_log(poap_script_log_handler, "Selected conf file name : %s" % config_file_src)
    except Exception as inst:
        poap_log(poap_script_log_handler, "Set src config filename location failed : %s " % inst)
        cleanup_files()
        poap_script_log_handler.close()
        exit(1)

def get_version ():
    msg = cli ("show version")
    lines = msg[1].split("\n")
    for line in lines:
        index=line.find("kickstart:")
        if (index!=-1):
            index=line.find("version")
            ver=line[index+8:]
            return ver

        index=line.find("system:")
        if (index!=-1):
            index=line.find("version")
            ver=line[index+8:]
            return ver

def get_bios_ver():
    msg = cli ("show version")
    lines = msg[1].split("\n")
    for line in lines:
        index=line.find("BIOS:")
        if (index!=-1):
            index=line.find("version")
            ver=line[index+8:index+13]
            return ver


def install_bios():
     try:
       cli ("config terminal ; terminal dont-ask")
       ret =  cli ("config terminal ; install all nxos %s bios" % system_image_dst)
       poap_log(poap_script_log_handler,"Bios successfully upgraded to version %s" % get_bios_ver())
     except Exception as inst:
       poap_log(poap_script_log_handler, "bios upgrade failed: %s" % inst)
       poap_log(poap_script_log_handler, "********** Traceback **********\n %s" % traceback.format_exc())
       cleanup_files()
       poap_script_log_handler.close()
       exit(1)

def is_bios_upgrade_needed():
  # check if image is to be upgraded to 7.x
  # Then check if bios is 2.x and current image vertion is 6.x
    global single_image_poap_flag,system_image_src
    ver = get_version()
    bios = get_bios_ver()
    poap_log(poap_script_log_handler, "Switch is running version %s with bios version %s system_image_src %s single_image_poap_flag %d" % (ver,bios,system_image_src,single_image_poap_flag))
    if (re.match("nxos.7",system_image_src)) :
        poap_log(poap_script_log_handler, "Upgrading to a nxos 7.x image")
        if (re.match("^6.0",ver) and re.match("^2.",bios)):
            poap_log(poap_script_log_handler, "Bios needs to be upgraded as switch is running 6.x version and bios version is less than 3.0")
            return True
    poap_log(poap_script_log_handler,"Bios upgrade not needed")
    return False

# Cleanup logfiles
poap_cleanup_script_logs()

if poap_config_file_mode == "poap_location":
	#set source config file based on location
        setSrcCfgFileNameLocation()

elif poap_config_file_mode == "poap_serial_number":
	#set source config file based on switch's serial number
        setSrcCfgFileNameSerial()

elif poap_config_file_mode == "poap_mac":
	#set source config file based on switch's interface MAC
        setSrcCfgFileNameMAC()

elif poap_config_file_mode == "poap_hostname":
	#set source config file based on switch's assigned hostname
        setSrcCfgFileNameHostName()

verifyfreespace()

# extract system and kickstart images from "show boot"
extractBootVar()

if (re.match("nxos.7",system_image_src)) :
    single_image_poap_flag = 1
else :
    single_image_poap_flag = 0

# copy config file and images
copyConfig()

# copy config file and images
copySystem()

if single_image_poap_flag != 1 :
   copyKickstart()

signal.signal(signal.SIGTERM, sig_handler_no_exit)

# install images
if single_image_poap_flag != 1 :
   installImages()
else:
   installImages_7_x()

if emptyFirstFile is 0:
	cli ('copy bootflash:%s scheduled-config' % config_file_dst_first)
	poap_log(poap_script_log_handler, "######### Copying the first scheduled cfg done ##########")
	#removeFile("/bootflash/%s" % config_file_dst_first)

cli ('copy bootflash:%s scheduled-config' % config_file_dst_second)
poap_log(poap_script_log_handler, "######### Copying the second scheduled cfg done ##########")
removeFile("/bootflash/%s" % config_file_dst_second)

poap_script_log_handler.close()
exit(0)
