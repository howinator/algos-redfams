def GenerateConfig(u):

    resources = [
        {
            'name': 'redorithms-postgres-instance',
            'type': 'sqladmin.v1beta4.instance',
            'properties': {
                'region': 'us-central1',
                'databaseVersion': 'POSTGRES_9_6',
                'settings': {
                    'tier': 'db-custom-2-8192',
                    'locationPreference': {
                        'zone': 'us-central1-f'
                    },
                    'ipConfiguration': {
                        'ipv4Enabled': True,
                        'authorizedNetworks': [
                            {
                                'name': 'Unizin Office',
                                'value': '198.214.63.124/32'
                            },
                            {
                                'name': 'Internal Network',
                                'value': '$(ref.instance-static-ip.address)'
                            }
                        ]
                    }
                }
            }
        },
        {
            'name': 'redorithms-database',
            'type': 'sqladmin.v1beta4.database',
            'properties': {
                'instance': '$(ref.redorithms-postgres-instance.name)',
                'name': 'algosreddit'
            }
        }
    ]
    return {'resources': resources}