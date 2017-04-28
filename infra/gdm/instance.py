COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'
PROJECT_NAME = 'algorithms-reddit'


def GenerateConfig(u):

    resources = [{
        'name': 'scrapehelp-vm',
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
                    'value': ''.join(['#!/usr/bin/env bash\n',
                                      'cd /tmp/\n',
                                      'git clone https://github.com/howinator/algos-redfams.git\n',
                                      'cp algos-redfams/infra/vm-init.sh ~\n',
                                      'cd ~\n',
                                      './vm-init.sh\n\n'
                                      ])
                }]
            },
            'serviceAccounts': [
                {
                    'email': '509708941669-compute@developer.gserviceaccount.com',
                    'scopes': ['https://www.googleapis.com/auth/cloud-platform']
                }
            ]
        }
    }, {
        'name': 'instance-static-ip',
        'type': 'compute.v1.address',
        'properties':{
            'name': 'instance-static-ip',
            'region': 'us-central1'
        }
    }]
    return {'resources': resources}
