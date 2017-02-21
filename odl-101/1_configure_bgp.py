#!/usr/bin/env python
from ydk.models.cisco_ios_xe.ned import Native
from ydk.providers import CodecServiceProvider
from ydk.services import CodecService
from defaults import *
import argparse
import requests
import sys

def send_xml(xml_string, host, port, user, pwd):
    url = ("http://{h}:{p}/restconf"
           "/config/network-topology:network-topology"
           "/topology/topology-netconf/node"
           "/CSR1K/yang-ext:mount/ned:native"
           "/router".format(h=host, p=port))

    headers = {'Content-Type': 'application/xml'}
    try:
        print url
        print xml_string
        result = requests.post(url, auth=(user, pwd), headers=headers, data=xml_string)
        print result
    except Exception:
        print(str(sys.exc_info()[0]))
        return -1
    return result

def serialize_model(model):
    provider = CodecServiceProvider(type="xml")
    codec = CodecService()
    return codec.encode(provider, model)

def create_instance(local_asn, n_ip, n_asn):
    bgp = Native().router.Bgp()
    bgp.id = 100
    n = bgp.Neighbor()
    n.id = '2.2.2.2'
    n.remote_as = 65100
    bgp.neighbor.append(n)
    return bgp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bgp_asn', default='', help="Local BGP AS Number")
    parser.add_argument('n_ip', default='', help="BGP Neighbor IP address")
    parser.add_argument('n_asn', default='', help="BGP Neighbor AS Number")
    parser.add_argument('--host', '-H', default=HOST, help="remote host address")
    parser.add_argument('--port', '-P', default=PORT, help="port")
    parser.add_argument('--user', '-u', default=USER, help="username")
    parser.add_argument('--password', '-p', default=PASS, help="password")
    args = parser.parse_args()

    bgp_instance = create_instance(args.bgp_asn, args.n_ip, args.n_asn)

    xml_string = serialize_model(bgp_instance)

    result = send_xml(xml_string, args.host, args.port, args.user, args.password)

    return result.text


if __name__ == '__main__':
    sys.exit(main())

