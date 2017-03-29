from ydk.types import Empty

#import pydevd
#pydevd.settrace('192.168.145.1', port=55555, stdoutToServer=True, stderrToServer=True)


def compare(state, expect_key, expect_value, result=True):
    if any(isinstance(expect_value, x) for x in [str, int, bool]):
        return expect_value == state
    elif state.__class__.__name__.endswith('Enum'):
        return state.name == expect_value.iterkeys().next()
    elif not expect_value or expect_key == 'parent':
        return True
    elif isinstance(expect_value, list):
        # value is list
        # need to make sure that for each element from the expect_value list there's a match in state list
        if not isinstance(state, list):
            raise ValueError('State object is not list: {}'.format(str(state)))
        for el in expect_value:
            result = result and any(compare(new_state, expect_key, el, result) for new_state in state)
        return result
    elif isinstance(expect_value, dict):
        # value is object
        # need to make sure that all expected non-None values have a match
        if not getattr(state, '__dict__'):
            raise ValueError('State object is not class instance: {}'.format(str(state)))
        for k, v in expect_value.iteritems():
            new_state = getattr(state, k)
            result = result and compare(new_state, k, v, result)
        return result
    else:
        return ValueError('Unexpected YAML value: {} of type {}'.format(expect_value, type(expect_value)))

def instantiate(binding, model_key, model_value, action='assign'):
    if isinstance(model_value, str) and model_value.lower() == 'empty':
        setattr(binding, model_key, Empty())
    elif any(isinstance(model_value, x) for x in [str, bool, int]):
        if action == 'return':
            return model_value
        elif action == 'assign':
            setattr(binding, model_key, model_value)
    elif isinstance(model_value, list):
        list_obj = getattr(binding, model_key.lower())
        for el in model_value:
                list_obj.append(instantiate(binding, model_key, el, action='return'))
    elif isinstance(model_value, dict):
        # special case handling enum type
        if all([x is None for x in model_value.values()]):
            enum_name = ''.join([x.capitalize() for x in model_key.split('_')]) + 'Enum'
            enum_class = getattr(binding, enum_name)
            for el in model_value.keys():
                enum = getattr(enum_class, el)
                if action == 'return':
                    return enum
                elif action == 'assign':
                    setattr(binding, model_key, enum)
        else:
            container = getattr(binding, model_key, None)
            if container and not isinstance(container, list):
                container_instance = container
            elif type(container).__name__ == 'YLeafList':
                container_instance = container
            else:
                model_key_camelized = ''.join([x.capitalize() for x in model_key.split('_')])
                container_instance = getattr(binding, model_key_camelized)()
            for k, v in model_value.iteritems():
                instantiate(container_instance, k, v, action='assign')
            if action == 'return':
                return container_instance
            elif action == 'assign':
                setattr(binding, model_key, container_instance)
    else:
        raise ValueError('Unexpected YAML value: {} of type {}'.format(model_value, type(model_value)))

class YdkModel:

    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.binding = None

    def configure(self):
        if self.model == 'interface':
            from ydk.models.ietf_ip_interface import ietf_interfaces
            self.binding = ietf_interfaces.Interfaces()
        elif self.model == 'interfaces-state':
            from ydk.models.ietf_ip_interface import ietf_interfaces
            self.binding = ietf_interfaces.InterfacesState()
        elif any(self.model == x for x in ['native']):
            from ydk.models.cisco_ios_xe.ned import Native
            self.binding = Native()
        elif self.model == 'junos':
            from ydk.models.junos_14_04.configuration import Configuration
            self.binding = Configuration()
        else:
            raise NotImplemented

        for k,v in self.data.iteritems():
            instantiate(self.binding, k, v)

    def verify(self, device):
        if self.model == 'interfaces-state':
            from ydk.models.ietf_ip_interface import ietf_interfaces
            self.binding = ietf_interfaces.InterfacesState()
        elif self.model == 'bgp-state':
            from ydk.models.cisco_ios_xe.cisco_bgp_state import BgpState
            self.binding = BgpState()
        else:
            raise NotImplemented
        root_key = ''.join([x.capitalize() for x in self.model.split('_')])
        model = self.action('read', device)
        return all(compare(model, k, v) for k,v in {root_key: self.data}.iteritems())

    def action(self, crud_action, device):
        if crud_action not in ['create','read']:
            raise ValueError(crud_action)
        from ydk.services import CRUDService
        from ydk.providers import NetconfServiceProvider
        provider = NetconfServiceProvider(address=device['hostname'],
                                          port=device['port'],
                                          username=device['username'],
                                          password=device['password'],
                                          protocol='ssh')
        crud = CRUDService()
        crud_instance = getattr(crud, crud_action)
        result = crud_instance(provider, self.binding)
        provider.close()
        return result

    def to_string(self):
        from ydk.providers import CodecServiceProvider
        from ydk.services import CodecService
        provider = CodecServiceProvider(type="xml")
        codec = CodecService()
        return codec.encode(provider, self.binding)


def bgp():
    import yaml
    test = """---
routing_options:
  autonomous_system:
    as_number: '65222'
policy_options:
  policy_statement:
    - name: CONNECTED->BGP
      from_:
        protocol:
          - ? direct
      then:
        accept: empty
protocols:
  bgp:
    group:
      - name: YANG
        export:
          - CONNECTED->BGP
        neighbor:
          - name: 12.12.12.1
            peer_as: '65111'
        """
    #device = {'hostname': '192.168.145.51', 'port': 830, 'username': 'admin', 'password': 'admin'}
    ydkmodel = YdkModel('junos', yaml.load(test))
    ydkmodel.configure()
    print ydkmodel.to_string()

def intf():
    import yaml
    expected_state = yaml.load("""---
  interface:
    - name: GigabitEthernet3
      oper_status:
        ? up""")
    device = {'hostname': '192.168.145.51', 'port': 830, 'username': 'admin', 'password': 'admin'}
    ydkmodel = YdkModel('interfaces-state', expected_state)
    print ydkmodel.verify(device)

if __name__ == '__main__':
    intf()

