class Paginator(object):
    data = None

    def __len__(self):
        """
        This is part of the implementation for len(Paginator_object)
        """
        return len(self.data) if self.data else 0

    offset = 0
    page_size = 25

    def __init__(self, offset=None, page_size=None):
        """
        The constructor for the paginator, takes optional arguments
        of offset and page_size. These have defaults, and will do the
        computations for starting and ending item indexes.
        """
        print "offset: %s" % offset
        if offset:
            print "setting offset."
            self.offset = offset
        if page_size:
            self.page_size = page_size

    @property
    def start_index(self):
        return self.offset * self.page_size

    @property
    def end_index(self):
        return ((self.offset + 1) * self.page_size)

    def create(self, data, total=None, **kwargs):
        self.data = data

        self.total = total

        for key, value in kwargs:
            self.__setattr__(key, value)
