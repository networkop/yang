# Example workflow of using YDK to verify operational state of IOS-XE devices

The following workflow verifies that:

1. Interface **GigabitEthernet3** is in `UP` state
2. BGP neighbor **12.12.12.3** is in the `established` state

## 1. Generate the YDK binding for IOS-XE with `bgp-state` YANG model

```bash
export YDKGEN_HOME=~/ydk-gen/
~/ydk-gen/generate.py --python --bundle cisco-ios-xe_0_1_2.json
pip install ~/ydk-gen/gen-api/python/cisco_ios_xe-bundle/dist/ydk-models-cisco_ios_xe-0.1.2.tar.gz
```

### 2. Verify operational state of interface **GigabitEthernet3**

```bash
./1_get_state.py interfaces
```


### 3. Verify operational state of BGP peering with **12.12.12.3**

```bash
./1_get_state.py bgp
```

## 4. (Optional) Verify that interface **GigabitEthernet3** is not in `down` state


```bash
cp nok.interfaces.yaml interfaces.yaml
./1_get_state.py interfaces
```
---

It is assumed that BGP peering is established between two IOS-XE devices

All defaults are setup in defaults.py configuration file
