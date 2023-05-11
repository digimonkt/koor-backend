import django_filters as filters

from .models import TenderDetails


class TenderDetailsFilter(filters.FilterSet):
    """
    `TenderDetailsFilter` is a filter class that filters `TenderDetails` queryset based on specified filter parameters.

    Attributes:
        - `country`: A filter for the `country field` of TenderDetails model.
        - `city`: A filter for the `city field` of TenderDetails model.
        - `opportunityType`: A filter for the `tender_type field` of TenderDetails model.
        - `deadline`: A filter for the `deadline field` of TenderDetails model.
        - `budget`: A filter for the budget_amount field of TenderDetails model.

    """

    country = filters.CharFilter(field_name='country__title', lookup_expr='iexact')
    city = filters.CharFilter(field_name='city__title', lookup_expr='iexact')
    deadline = filters.DateFilter(field_name='deadline')
    budget = filters.RangeFilter(field_name='budget_amount', lookup_expr='iexact')

    class Meta:
        model = TenderDetails
        fields = ['country', 'city', 'opportunityType', 'deadline', 'budget']
