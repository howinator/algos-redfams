def GenerateConfig(u):

    resources = [{
        'name': 'redorithms-postgres-instance',
        'type': 'sqladmin.v1beta4.instance',
        'properties':{
            'region': 'us-central1',
            'databaseVersion': 'POSTGRES_9_6',
            'settings': {
                'tier': 'db-custom-2-8192',
                'locationPreference': {
                    'zone': 'us-central1-f'
                }
            }
        }
    }]
    return {'resources': resources}