#!/usr/bin/env python

import pyangbind.lib.pybindJSON as pybindJSON
from binding import ietf_interfaces
from defaults import *
from helpers import *
import argparse
import yaml
import sys

def make_json(intf,conf):
    model = ietf_interfaces()
    intf_model = model.interfaces.interface.add(intf)
    intf_model.description = conf['description']
    ip_model = intf_model.ipv4.address.add(conf['address']['prefix'])
    ip_model.netmask = conf['address']['netmask']
    return pybindJSON.dumps(model, mode = 'ietf') 
       
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', '-i', default=YML, help="YAML Interface configuration file")
    args = parser.parse_args()

    yml = yaml.load(read_file(args.interface))
    
    for intf,conf in yml['interface'].iteritems():
        json = make_json(intf, conf)
        write_file('interface.json', json)

if __name__ == '__main__':
    sys.exit(main())
