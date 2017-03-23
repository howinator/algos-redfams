def GenerateConfig(unused_context):
    """Creates the network."""

    resources = [{
        'name': 'algos-reddit-network',
        'type': 'compute.v1.network',
        'properties': {
            'IPv4Range': '10.0.0.1/16',
            'description': 'Network for algorithms reddit project',
            'name': 'redorithms-network'
        }
    }]
    return {'resources': resources}
