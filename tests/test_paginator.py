import unittest

from mapmyfitness.utils.paginator import Paginator


def list_generator(start, end):
    return [i for i in range(start, end)]


class PaginatorTest(unittest.TestCase):


    def test_paginator_return_object(self):
        p = Paginator(offset=0, page_size=10)
        
        results = list_generator(p.start_index, p.end_index)

        p.create(results, total=10)

        assert len(p) == len(results)
        assert p.end_index > 0

    def test_paginator_second_page(self):
        pag = Paginator(offset=1, page_size=25)

        results = list_generator(pag.start_index, pag.end_index)

        pag.create(results, total=100)

        assert len(pag) == len(results)
        assert pag.start_index == 25
        assert pag.data[0] == 25
