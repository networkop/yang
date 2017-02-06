#!/usr/bin/env python

from ncclient import manager
from defaults import *
from helpers import *
import argparse
import sys

def edit_config(xml, host, port, user, pwd):
    with manager.connect(host=host, port=port, username=user, password=pwd,
                         hostkey_verify=False, device_params={'name': 'csr'}) as m:
        reply = m.edit_config(target='running', config=xml)
    return reply

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', '-i', default=XML, help="XML Interface configuration file")
    parser.add_argument('--host', '-H', default=HOST, help="remote host address")
    parser.add_argument('--port', '-P', default=PORT, help="port")
    parser.add_argument('--user', '-u', default=USER, help="username")
    parser.add_argument('--password', '-p', default=PASS, help="password")
    args = parser.parse_args()

    xml = read_file(args.interface)
    reply = edit_config(xml, args.host, args.port, args.user, args.password)
    print('Command sent: {}'.format(reply.ok))

if __name__ == '__main__':
    sys.exit(main())
