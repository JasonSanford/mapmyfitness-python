class PaginatorMetaClass(type):
    """
    The PaginatorMetaClass will allow nifty things like 
    len(paginator_object)
    """
    def __len__(self):
        return self.clslength()


class Paginator(object):
    __metaclass__ = PaginatorMetaClass

    data = None

    @classmethod
    def clslength(cls):
        """
        This is part of the implementation for len(Paginator_object)
        """
        return len(cls.data) if cls.data else 0


    offset = 0
    page_size = 25

    def __init__(self, offset=None, page_size=None):
        """
        The constructor for the paginator, takes optional arguments
        of offset and page_size. These have defaults, and will do the
        computations for starting and ending item indexes.
        """
        if offset:
            self.offset = offset
        if page_size:
            self.page_size = page_size

    @property
    def start_index(self):
        return self.offset

    @property
    def end_index(self):
        return ( (self.offset + 1) * self.page_size)

    def create(self, data, total=None, **kwargs):
        for key, value in kwargs:
            self.__setattr__(key, value)

        self.total = total
