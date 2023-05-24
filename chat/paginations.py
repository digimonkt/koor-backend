from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class LinkPagination(pagination.PageNumberPagination):
    """
    A custom pagination class that adds 'next' and 'previous' links to the paginated response.

    Attributes:
        page_size (int): The number of items to include on each page.
        page_size_query_param (str): The query parameter used to set the page size.
        max_page_size (int): The maximum allowed page size.
        page_query_param (str): The query parameter used to set the page number.

    Methods:
        get_next_link(): Returns the URL for the next page of results, or None if there is no next page.
        get_previous_link(): Returns the URL for the previous page of results, or None if there is no previous page.
        get_paginated_response(data): Returns a paginated response with 'next' and 'previous' links.
    """
    
    def get_next_link(self):
        """
        Returns the URL for the next page of results, or None if there is no next page.

        Returns:
            str or None: The URL for the next page of results, or None if there is no next page.

        """
        
        if not self.page.has_next():
            return None
        url = self.request.path
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        """
        Returns the URL for the previous page of results, or None if there is no previous page.

        Returns:
            str or None: The URL for the previous page of results, or None if there is no previous page.

        """
        
        if not self.page.has_previous():
            return None
        url = self.request.path
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
    
    def get_paginated_response(self, data):
        """
        Returns a paginated response with 'next' and 'previous' links.

        Args:
            data (list): The list of paginated items.

        Returns:
            Response: A response with 'next' and 'previous' links and the paginated items.

        """
        
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })