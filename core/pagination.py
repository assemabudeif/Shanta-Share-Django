from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StanderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        """
        Customize the paginated response to include `page_count`.
        """
        page = self.page
        return Response({
            'count': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'page_count': self.page.paginator.num_pages,
            'current_page': page.number,
            'results': data
        })