from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
import math

class PageNumberPaginationWithPageCount(PageNumberPagination):
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_count', self.page.paginator.num_pages),
            ('results', data),
            ('current', self.request.query_params.get(self.page_query_param, 1))
        ]))