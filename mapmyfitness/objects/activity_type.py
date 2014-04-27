from .base import BaseObject


class ActivityTypeObject(BaseObject):
    simple_properties = {
        'name': None
    }

    @property
    def id(self):
        return int(self.original_dict['_links']['self'][0]['id'])

    @property
    def has_parent(self):
        return self.id != self.root_activity_type_id

    @property
    def root_activity_type_id(self):
        return int(self.original_dict['_links']['root'][0]['id'])

    @property
    def root_activity_type(self):
        if not self.has_parent:
            return self
        if hasattr(self, '_activity_type'):
            return self._activity_type
        else:
            from mapmyfitness import MapMyFitness
            instance = MapMyFitness.instance()
            activity_type = instance.activity_type.find(self.root_activity_type_id)
            self._activity_type = activity_type
            return self._activity_type
