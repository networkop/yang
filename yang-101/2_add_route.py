#!/usr/bin/env python
import pyangbind.lib.pybindJSON as pybindJSON
from defaults import *
from helpers import *
import argparse
import binding
import netaddr
import requests
import sys

def get_routes(host, port, user, pwd):
    url = "http://{h}:{p}/restconf/api/config/native/ip/route?deep".format(h=host, p=port)
    headers = {'accept': 'application/vnd.yang.data+json'}
    try:
        result = requests.get(url, auth=(user, pwd), headers=headers)
    except Exception:
        print(str(sys.exc_info()[0]))
        return -1
    return result.text

def add_route(current_routes, route, nh, name):
    try: 
        model = pybindJSON.loads_ietf(current_routes, binding, "cisco_route_static")
        route = model.route.ip_route_interface_forwarding_list.add(route)
        nexthop = route.fwd_list.add(nh)
        nexthop.name = name
        json_data = pybindJSON.dumps(model, mode='ietf')
        write_file('{}.json'.format(NEW_FN), json_data)
    except Exception:
        print(str(sys.exc_info()[0]))
        return -1
    return json_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('route', default='', help="New static route in prefix/length format")
    parser.add_argument('nexthop', default='', help="Next-hop of the new static route(IPv4 address of Interface name)")
    parser.add_argument('--name', '-n', default='', help="Optional name for a static route")
    parser.add_argument('--host', '-H', default=HOST, help="remote host address")
    parser.add_argument('--port', '-P', default=PORT, help="port")
    parser.add_argument('--user', '-u', default=USER, help="username")
    parser.add_argument('--password', '-p', default=PASS, help="password")
    args = parser.parse_args()

    current_routes = get_routes(args.host, args.port, args.user, args.password)
    ip = netaddr.IPNetwork(args.route)
    route = ' '.join([str(ip.network), str(ip.netmask)])
    result = add_route(current_routes, route, args.nexthop, args.name)    
    print result



if __name__ == '__main__':
    sys.exit(main())

