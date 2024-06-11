from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = settings.DEFAULT_PAGE_SIZE

class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'current': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'total_records': self.page.paginator.count,
            'results': data
        })