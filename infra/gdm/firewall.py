def GenerateConfig(u):

    resources = [{
        'name': 'a-firewall-rule',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(ref.algos-reddit-network.selfLink)',
            'sourceRanges': ['0.0.0.0/0'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': [80]
            }]
        }
    }, {
        'name': 'b-firewall-rule',
        'type': 'compute.v1.firewall',
        'properties': {
            'network': '$(regf.algos-reddit-network.selfLink)'
            'sourceRanges': ['$(ref.algos-reddit-network.IPv4Range)'],
            'allowed': [{
                'IPProtocol': 'TCP',
                'ports': ['0-65535']
            }]
        }
    }]
    return {'resources': resources}
