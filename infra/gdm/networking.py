def GenerateConfig(unused_context):

    resources = [{
        'name': 'network-1',
        'type': 'network.py'
    }, {
        'name': 'firewall',
        'type': 'firewall.py'
    }]
    return {'resources': resources}
