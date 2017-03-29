from ansible.module_utils.basic import AnsibleModule
from ydk_yaml import YdkModel


def main():
    arguments = dict(
        hostname=dict(type='str'),
        model=dict(type='str'),
        data=dict(type='dict'),
        action=dict(type='str'),
        username=dict(type='str'),
        password=dict(type='str')
    )
    module = AnsibleModule(
        argument_spec = arguments,
        supports_check_mode=True
        )

    ydk_model = YdkModel( module.params['model'], module.params['data'])

    ydk_action = getattr(ydk_model, module.params['action'])

    device = {'hostname': module.params['hostname'], 'port': 830,
              'username':  module.params['username'],
              'password':  module.params['password']}

    rc = ydk_action(device)
    if rc and module.params['action'] == 'configure':
        module.exit_json(changed=True)
    elif rc and module.params['action'] == 'verify':
        module.exit_json(changed=False)
    else:
        module.fail_json(msg="YDK module has failed with action {}".format(module.params['action']))

if __name__ == '__main__':
    main()
