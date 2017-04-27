COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'
PROJECT_NAME = 'algorithms-reddit'


def GenerateConfig(u):

    resources = [{
        'name': 'scraper-vm',
        'type': 'compute.v1.instance',
        'properties': {
            'zone': 'us-central1-f',
            'machineType': ''.join([COMPUTE_URL_BASE, 'projects/', PROJECT_NAME,
                                    '/zones/us-central1-f/', 'machineTypes/g1-small']),
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': ''.join([COMPUTE_URL_BASE, 'projects/',
                                            'ubuntu-os-cloud/global/',
                                            'images/ubuntu-1604-xenial-v20170307'])
                }
            }],
            'networkInterfaces': [{
                'network': '$(ref.algos-reddit-network.selfLink)',
                'accessConfigs': [{
                    'name': 'External NAT',
                    'type': 'ONE_TO_ONE_NAT',
                    'natIP': '$(ref.instance-static-ip.address)'
                }]
            }],
            'metadata': {
                'items': [{
                    'key': 'startup-script',
                    'value': ''.join
                }]
            }
        }
    }, {
        'name': 'instance-static-ip',
        'type': 'compute.v1.address',
        'properties':{
            'name': 'instance-staic-ip',
            'region': 'us-central1'
        }
    }]
    return {'resources': resources}
