from ydk.types import Empty


def instantiate(binding, model_key, model_value, action='assign'):
    if any(isinstance(model_value, x) for x in [str, bool, int]):
        setattr(binding, model_key, model_value)
    elif model_value is None:
        setattr(binding, model_key, Empty())
    elif isinstance(model_value, list):
        model_key = model_key.lower()
        for el in model_value:
            getattr(binding, model_key).append(instantiate(binding, model_key, el, action='return'))
    elif isinstance(model_value, dict):
        container = getattr(binding, model_key)
        if container and not isinstance(container, list):
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
        raise NotImplemented(model_value)

class YdkModel:

    def __init__(self, model, data):
        self.model = model
        self.data = data
        if model == 'interface':
            from ydk.models.ietf_ip_interface import ietf_interfaces
            self.binding = ietf_interfaces.Interfaces()
        elif any(model == x for x in ['bgp', 'ospf', 'interface_native']):
            from ydk.models.cisco_ios_xe.ned import Native
            self.binding = Native()
        else:
            raise NotImplemented(model)
        for k,v in self.data.iteritems():
            instantiate(self.binding, k, v)

    def verify(self):
        raise NotImplementedError

    def action(self, crud_action, device):
        if crud_action not in ['create']:
            raise NotImplemented(crud_action)
        from ydk.services import CRUDService
        from ydk.providers import NetconfServiceProvider
        provider = NetconfServiceProvider(address=device['hostname'],
                                          port=device['port'],
                                          username=device['username'],
                                          password=device['password'],
                                          protocol='ssh')
        crud = CRUDService()
        crud_instance = getattr(crud, crud_action)
        crud_instance(provider, self.binding)
        provider.close()
        return

    def to_string(self):
        from ydk.providers import CodecServiceProvider
        from ydk.services import CodecService
        provider = CodecServiceProvider(type="xml")
        codec = CodecService()
        return codec.encode(provider, self.binding)

