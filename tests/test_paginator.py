from mapmyfitness.utils.paginator import Paginator


class PaginatorTest(object):

    def list_generator(start, end):
        return [i for i in range(start, end)]

    def test_paginator_return_object(self):
        p = Paginator(offset=0, page_size=10)
        
        results = self.list_generator(p.start_index, p.end_index)

        p.create(results, total=10)

        assert len(p) == len(results)
        assert p.end_index > 0
