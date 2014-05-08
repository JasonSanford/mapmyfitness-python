import copy

from mapmyfitness.exceptions import InvalidSearchArgumentsException, InvalidObjectException
from mapmyfitness.paginator import Paginator


class Deleteable(object):
    def delete(self, id):
        self.call('delete', '{0}/{1}'.format(self.path, id))


class Searchable(object):
    def _search(self, params):
        api_resp = self.call('get', self.path + '/', params=params)

        objs = []
        for obj in api_resp['_embedded'][self.embedded_name]:
            serializer = self.serializer_class(obj)
            objs.append(serializer.serialized)
        self.total_count = api_resp['total_count']
        return objs

    def search(self, per_page=40, **kwargs):
        original_kwargs = copy.deepcopy(kwargs)
        self.per_page = per_page
        kwargs.update({'limit': self.per_page})
        self.validator = self.validator_class(search_kwargs=kwargs)
        if not self.validator.valid:
            raise InvalidSearchArgumentsException(self.validator)
        if self.__class__.__name__ == 'Route':
            # Routes are special, and need to be requested with additional params
            kwargs.update({'field_set': 'detailed'})
        #
        # This feels a little hacky but, we need to make the initial call
        # to the API to get the total count needed to process pages
        #
        initial_object_list = self._search(kwargs)
        return Paginator(initial_object_list, self.per_page, self.total_count, self, original_kwargs)

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
    def _cache_name(self, id):
        return '{}_{}'.format(self.__class__.__name__, id)

    def find(self, id):
        cache_name = self._cache_name(id)
        if self.cache_finds and hasattr(self, cache_name):
            return getattr(self, cache_name)
        else:
            params = None
            if self.__class__.__name__ == 'Route':
                # Routes are special, and need to be requested with additional params
                params = {'field_set': 'detailed'}
            api_resp = self.call('get', '{0}/{1}'.format(self.path, id), params=params)
            serializer = self.serializer_class(api_resp)
            serialized = serializer.serialized
            if self.cache_finds:
                setattr(self, cache_name, serialized)
                return getattr(self, cache_name)
            else:
                return serialized
