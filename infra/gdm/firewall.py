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
    }]
    return {'resources': resources}
