## Workflow example:

### 1. Get device capabilities  

```bash
./1_get_capabilities.py
```

### 2. Download YANG models  

```bash
./2_get_yang.py -y ietf-ip ietf-interfaces ietf-inet-types ietf-yang-types
```

### 3. Generate python bindings  

```bash
pyang --plugindir $PYBINDPLUGIN -f pybind -o ietf_ip.py ietf-ip.yang ietf-interfaces.yang ietf-inet-types.yang ietf-inet-types.yang
```

### 4. Generate JSON configuration file  

```bash
./3_make_json.py
```

### 5. Convert JSON to XML  

```bash
pyang -f jtox -o interface.jtox ietf-ip.yang ietf-interfaces.yang ietf-inet-types.yang ietf-yang-types.yang
json2xml -t config -o interface.xml interface.jtox interface.json
```

### 6. Edit running configuration on the device  

```bash
./4_send_xml.py
```

---

All defaults are setup in defaults.py configuration file

