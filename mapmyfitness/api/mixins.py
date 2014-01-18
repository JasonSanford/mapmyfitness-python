from mapmyfitness.exceptions import InvalidSearchArgumentsException, InvalidObjectException


class Deleteable(object):
    def delete(self, id):
        self.call('delete', '{0}/{1}'.format(self.path, id))


class Searchable(object):
    def search(self, **kwargs):
        self.validator = self.validator_class(search_kwargs=kwargs)
        if not self.validator.valid:
            raise InvalidSearchArgumentsException(self.validator)
        if self.__class__.__name__ == 'Route':
            # Routes are special, and need to be requested with additional params
            kwargs.update({'field_set': 'detailed'})
        api_resp = self.call('get', self.path + '/', params=kwargs)

        objs = []
        for obj in api_resp['_embedded'][self.embedded_name]:
            serializer = self.serializer_class(obj)
            objs.append(serializer.serialized)
        return objs


class Createable(object):
    def create(self, obj):
        self.validator = self.validator_class(create_obj=obj)
        if not self.validator.valid:
            raise InvalidObjectException(self.validator)

        inflator = self.inflator_class(obj)
        data = inflator.inflated

        params = None
        if self.__class__.__name__ == 'Route':
            # Routes are special, and need to be created with additional params
            params = {'field_set': 'detailed'}

        api_resp = self.call('post', '{0}/'.format(self.path), data=data, extra_headers={'Content-Type': 'application/json'}, params=params)

        serializer = self.serializer_class(api_resp)
        return serializer.serialized


class Updateable(object):
    def update(self, id, obj):
        self.validator = self.validator_class(obj)
        if not self.validator.valid:
            raise InvalidObjectException(self.validator)

        inflator = self.inflator_class(obj)
        data = inflator.inflated

        api_resp = self.call('put', '{0}/{1}/'.format(self.path, id), data=data, extra_headers={'Content-Type': 'application/json'})
        serializer = self.serializer_class(api_resp)
        return serializer.serialized


class Findable(object):
    def find(self, id):
        params = None
        if self.__class__.__name__ == 'Route':
            # Routes are special, and need to be requested with additional params
            params = {'field_set': 'detailed'}
        api_resp = self.call('get', '{0}/{1}'.format(self.path, id), params=params)
        serializer = self.serializer_class(api_resp)
        return serializer.serialized
