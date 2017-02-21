## Example workflow of using YDK and Opendaylight to modify BGP configuration on Cisco IOS XE

### 1. (Optional) Check the IOS XE device IP and credentials
```bash
cat new_device.xml.2
```

## 2. Connect the device to OpenDaylight
```bash
curl -v -k -u admin:admin -H "Content-Type: application/xml" -X POST \
http://localhost:8181/restconf/config/network-topology:network-topology\
/topology/topology-netconf/node/controller-config/yang-ext:mount/config:modules\
 -d @new_device.xml.2
```

### 3. Check that the status has changed to `connected`
```bash
curl -v -k -u admin:admin http://localhost:8181/restconf/operational\
/network-topology:network-topology/ | python -m json.tool
```

### 4. (Optional) In case the connection has failed, delete the device
```bash
curl -v -k -u admin:admin -X DELETE \
http://localhost:8181/restconf/config/network-topology:network-topology\
/topology/topology-netconf/node/controller-config/yang-ext:mount/config:modules\
/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/CSR1K
```

### 5. Install YDK and its dependencies
```bash
git clone https://github.com/CiscoDevNet/ydk-gen.git ~/ydk-gen
pip install -r ~/ydk-gen/requirements.txt
export YDKGEN_HOME=~/ydk-gen/
~/ydk-gen/generate.py --python --core
pip install ~/ydk-gen/gen-api/python/ydk/dist/ydk-0.5.3.tar.gz
```

### 6. Create Python binding for IOS XE's native YANG model
```bash
~/ydk-gen/generate.py --python --bundle cisco-ios-xe_0_1_0.json -v
pip install ~/ydk-gen/gen-api/python/cisco_ios_xe-bundle/dist/ydk-models-cisco_ios_xe-0.1.0.tar.gz

```

### 7. Use the script to create an BGP instance with a single neighbor
```bash
./1_configure_bgp.py  100 2.2.2.2 123
```

---

All defaults are setup in defaults.py configuration file

