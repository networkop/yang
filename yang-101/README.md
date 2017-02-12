## Example workflow of using RESTCONF to modify existing static routes

### 1. (Optional) Get the current configuration of static routes 
```bash
curl -v -k -u admin:admin -H "Accept: application/vnd.yang.data+json" http://192.168.145.51/restconf/api/config/native/ip/route?deep > current.json
```

## 2. Generate Python bindings based on the YANG model
```bash
pyang --plugindir $PYBINDPLUGIN -f pybind -o binding.py cisco-route-static.yang
```

### 3. (Option 1) Use generated Python binding to change the next hop of an existing static route (e.g. from GigabitEthernet2 to 12.12.12.2)
```bash
./1_change_nexthop.py 1.1.1.1/32 GigabitEthernet2 12.12.12.2
```

### 4. (Option 2) Use generated Python binding to add a new static route
```bash
./2_add_route.py -n NEW-ROUTE-NAME 4.4.4.0/24 12.12.12.2
```

### 5. Convert JSON file generated at step 3 or 4 to XML (this step can be skipped once CSCvc09320 gets resolved)
```bash
pyang -f jtox -o static-route.jtox cisco-route-static.yang
./json2xml -t restconf -o new_conf.xml static-route.jtox new_conf.json
```

### 6. Send generated XML via RESTCONF
```bash
curl -v -k -u admin:admin -H "Content-Type: application/vnd.yang.data+xml" \
 -X PUT http://192.168.145.51/restconf/api/config/native/ip/route/ -d @new_conf.xml
```

---

All defaults are setup in defaults.py configuration file
