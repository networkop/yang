## Example workflow of configuring NETCONF devices using YAML configuration files

### 1. Examine the structure of the OSPF YANG model
```bash
pyang -f tree --tree-path "/native/router/ospf" ~/odl-0.5.2/cache/schema/ned\@2016-10-24.yang -o ospf.tree
```

### 2. Create a YAML file following the structure of the OSPF YANG model
```bash
cat ospf.yaml
```

### 3. Update device's OSPF configuration
```bash
./1_send_yaml.py ospf ospf.yaml
```

### 4. Repeat steps [1 - 3] for other configuration elements (e.g. interface and BGP)
```bash
./1_interface.py interface_native interface.yaml

./1_send_yaml.py ospf ospf.yaml
```

---

All defaults are setup in defaults.py configuration file

