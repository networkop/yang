#!/usr/bin/env python

import xml.etree.ElementTree as ET
from ncclient import manager
import argparse
import sys
import re


HOST = '10.6.143.3'
PORT = 830
USER = 'admin'
PASS = 'admin'

def get_schema(host, port, user, pwd, schema):
    with manager.connect(host=host, port=port, username=user, password=pwd,
                         hostkey_verify=False, device_params={'name': 'csr'}) as m:
            schema = m.get_schema(schema)
            xml_et = ET.fromstring(schema.xml)
            yang = list(xml_et)[0].text

    return yang

def write_file(fn, text):
    with open(fn, 'w') as f:
        f.write(text) 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', default=HOST, help="remote host address")
    parser.add_argument('--port', '-P', default=PORT, help="port")
    parser.add_argument('--user', '-u', default=USER, help="username")
    parser.add_argument('--password', '-p', default=PASS, help="password")
    parser.add_argument('--yang', '-y', nargs = '*', help="List of yang models")
    args = parser.parse_args()

    for yang in args.yang:
        yang_text = get_schema(args.host, args.port, args.user, args.password, yang)
        write_file('{}.yang'.format(yang), yang_text)


if __name__ == '__main__':
    sys.exit(main())
