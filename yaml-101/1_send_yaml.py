#!/usr/bin/env python
from defaults import *
from helpers import *
from ydk_yaml import YdkModel
import argparse
import yaml
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model', default='', help="Name of YANG model to instantiate")
    parser.add_argument('data', default='', help="YAML file containing configuration data")
    parser.add_argument('--host', '-H', default=HOST, help="remote host address")
    parser.add_argument('--port', '-P', default=PORT, help="port")
    parser.add_argument('--user', '-u', default=USER, help="username")
    parser.add_argument('--password', '-p', default=PASS, help="password")
    args = parser.parse_args()

    device = { 'hostname' : args.host, 'port' : args.port, 'username' : args.user, 'password' : args.password }

    data_parsed = yaml.load(read_file(args.data))
     
    interface = YdkModel(args.model, data_parsed)

    print interface.to_string()

    interface.action('create', device)


if __name__ == '__main__':
    sys.exit(main())

