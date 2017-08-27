# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:54:53 2017

@author: jc2450
"""
import sys
import re
import os

from jinja2 import Template

# Setup
OVPN_DIR = 'C://OpenVPN'
CFG_PATH = os.path.join(*(OVPN_DIR,'config'))
RSA_PATH = os.path.join(*(OVPN_DIR,'easy-rsa'))
KEY_PATH = os.path.join(*(RSA_PATH,'keys'))


def make_config(device_name, flags={'no_gateway': False, 'windows_flag': True}):
    # Find VPN subnet address
    with open(os.path.join(*(CFG_PATH,"server.ovpn")), "r") as cfg_file:
        cfg_lines = cfg_file.readlines()
    
    cfg_data = [line.split(" ") for line in cfg_lines]
    svr_data = [line for line in cfg_data if line[0]=="server"]

    # Load client key file
    try:
        key_file = open(os.path.join(*(KEY_PATH,"{0}.key".format(device_name))), "r")
        key_data = key_file.read()
    except:
        sys.exit("Key file not found for this device. Ensure certs have been created and the device name is entered correctly.")
    
    # Load client certificate
    try:
        crt_file = open(os.path.join(*(KEY_PATH,"{0}.crt".format(device_name))), "r")
        crt_read = crt_file.read()
        crt_data=re.split(r'.(?=\n-----BEGIN CERTIFICATE-----)' ,crt_read)[1][1:]
    except:
        sys.exit("Cert file not found for this device. Ensure certs have been created and the device name is entered correctly.")
    
    # Load server ca
    try:
        ca_file = open(os.path.join(*(KEY_PATH,"ca.crt")), "r")
        ca_data = ca_file.read()
    except:
        sys.exit("CA file not found for this device. Ensure certificate authority crt is in the working directory.")
    
    # Open and fill out template config
    template_path = os.path.join("configs","config.template")
    template_file = open(template_path, "r")
    model = Template(template_file.read(), trim_blocks=True)
    
    config_data=model.render(flags=flags, ca=ca_data, crt=crt_data, key=key_data)
    
    # Save generated config file
    if flags['no_gateway']:
        gateway_name = 'local'
    else:
        gateway_name = 'internet'
        
    config_path = os.path.join("configs","jtcvpn-{0}-{1}.ovpn".format(device_name, gateway_name))
    config_file = open(config_path, "w")
    config_file.write(config_data) 
    config_file.close()


if __name__ == "__main__":
    print("This script assumes your VPN is set up for routing all traffic.\nTwo versions of the config are generated, one leaves pushed routes intact, the other suppresses all pushed routes and only sets up local subnet routing.")
    
    # Input arguments
    dev_name = str(input("Enter device name:"))
    
    # Ask if Windows device
    is_windows = str(input("Is this a Windows device? (y/n):"))
    if is_windows is "y":
        is_windows_flag = True
    else:
        is_windows_flag = False
    
    make_config(dev_name, flags={'no_gateway': False, 'windows_flag': is_windows_flag})
    make_config(dev_name, flags={'no_gateway': True, 'windows_flag': is_windows_flag})