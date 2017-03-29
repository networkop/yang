#!/usr/bin/env python
from defaults import *
from helpers import *
import yaml
from ydk_yaml import YdkModel
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model', default='', help="model to check (bgp or interfaces)")
    parser.add_argument('--host', '-H', default=HOST, help="remote host address")
    parser.add_argument('--port', '-P', default=PORT, help="port")
    parser.add_argument('--user', '-u', default=USER, help="username")
    parser.add_argument('--password', '-p', default=PASS, help="password")
    args = parser.parse_args()

    device = { 'hostname' : args.host, 'port' : args.port, 'username' : args.user, 'password' : args.password }

    expected_state = yaml.load(read_file('{}.yaml'.format(args.model)))

    state_model = args.model + '-state'

    ydkmodel = YdkModel(state_model, expected_state)

    if ydkmodel.verify(device):
        return "State matches the input"
    else:
        return "State does not match the input"



if __name__ == '__main__':
    sys.exit(main())

