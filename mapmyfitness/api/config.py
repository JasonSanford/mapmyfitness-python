class APIConfig(object):
    uri_root = 'https://oauth2-api.mapmyapi.com'

    def __init__(self, api_key, access_token):

        self.api_key = api_key
        self.access_token = access_token
        self.api_root = '{0}/v7.0'.format(self.uri_root)
