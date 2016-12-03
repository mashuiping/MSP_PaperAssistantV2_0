#!/usr/bin/python
# filename: macmgr.py
"""        Module for Changing the MAC on Openwrt

    This module read and write to file '/etc/config/network'.

    =========       Write By NanPuYue       =========

    Example:
        get_line_of_mac("'wan'")
        change_mac("'wan'",'70:CB:69:F8:6C:C6')
        add_mac("'lan'",'70:CB:69:F8:6C:C7')

    Note: The name of Interface must like this:
        "'wan'" or "'lan'"
"""


import os
__name__ = ["macmgr"]

def read_config():
    config_file = open('/etc/config/network','r')
    config_list = config_file.readlines()
    config_file.close()
    return config_list

def seek_in_list(target,list_name,start_number):
    length = len(list_name)-1
    for i in range(start_number, length):
        if target in list_name[i]:
            break
    if target in list_name[i]:
        return i
    else:
        return -1

def get_info_of(interface):
    config_list = read_config()
    a = seek_in_list('config interface '+interface,config_list,0)
    b = seek_in_list('config',config_list,a+1)
    if b == -1:
        config_list_light = config_list[a:]
    else:
        config_list_light = config_list[a:b]
    c = seek_in_list('option macaddr',config_list_light,0)
    if 'option macaddr' in config_list_light[c]:
        return a+c
    else:
	return -1


def save_config(config_list):
    config_file = open('/etc/config/network','w')
    config_file.writelines(config_list)
    config_file.close()
    
def add_mac(interface,macaddr):
    config_list = read_config()
    i = seek_in_list('config interface '+interface,config_list,0)
    if i == -1:
        print 'No config of interface '+interface+'found !'
        exit()
    config_list.insert(i+1,'\toption macaddr '+"'"+macaddr+"'\n")
    save_config(config_list)

def change_mac(interface,macaddr):
    i = get_info_of(interface)
    if i == -1:
    	add_mac(interface,macaddr)
    else:
	config_list = read_config()
	if macaddr not in config_list[i]:
            config_list[i] = '\toption macaddr '+"'"+macaddr+"'\n"
            save_config(config_list)

def apply_mac():
    print 'Waiting for Applying MAC Address...'
    os.system('/etc/init.d/network restart')

def get_line_of_mac(interface):
    config_list = read_config()
    i = get_info_of(interface)
    if i == -1:
        return 'None'
    else:
        return config_list[i]

