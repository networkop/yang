# Example workflow of using YDK to configure JUNOS devices

Each of the following two workflows accomplish the same thing:

* Configure `ge-0/0/0` and `lo0` interfaces
* Configure BGP peering with device `12.12.12.1` in remote-as `65111`
* Export IP prefix of `lo0` into BGP RIB

## (Option A) JUNOS native YANG model

Option A uses JUNOS native [YANG model](https://github.com/Juniper/yang)
### 1. Generate and install YDK bindings for JUNOS native data model

```bash
export YDKGEN_HOME=~/ydk-gen/
~/ydk-gen/generate.py --python --bundle junos-14_02-oper-0_1_1.json
pip install ~/ydk-gen/gen-api/python/junos_14_04-bundle/dist/ydk-models-junos_14_04-0.1.0.tar.gz
```

### 2. Examine interface and BGP configuration files and make changes if necessary

```bash
cat interface.yaml
cat bgp.yaml
```

### 3. Push interface and BGP configuration changes to the devices

```bash
./1_send_yaml.py junos interface.yaml
./1_send_yaml.py junos bgp.yaml
```

## (Option B) OpenConfig YANG model

Option B uses OpenConfig [YANG models](https://github.com/openconfig/public)

### 1. Generate and install YDK bindings for OpenConfig YANG models

```bash
export YDKGEN_HOME=~/ydk-gen/
~/ydk-gen/generate.py --python --bundle openconfig-config_0_1_1.json
pip install ~/ydk-gen/gen-api/python/openconfig_bgp_policy-bundle/dist/ydk-models-openconfig_bgp_policy-0.1.1.tar.gz
```

### 2. Examine interface and BGP configuration files and make changes if necessary

```bash
oc-bgp.yaml
oc-interface.yaml
oc-policy.yaml
```

### 3. Push interface, routing policy and BGP configuration changes to the devices

```bash
./1_send_yaml.py openconfig-interfaces oc-interface.yaml
./1_send_yaml.py openconfig-policy oc-policy.yaml
./1_send_yaml.py openconfig-bgp oc-bgp.yaml
```

---

All workflows were tested on vMX 17.1R1.8

OpenConfig needs to be installed as a separate package as described [here](https://www.juniper.net/documentation/en_US/junos/topics/task/installation/openconfig-installing.html)

All defaults are setup in defaults.py configuration file
