import django_filters as filters

from .models import JobDetails

class JobDetailsFilter(filters.FilterSet):
    """A filter set for querying job details based on various criteria.

    This filter set allows for filtering job details based on the following criteria:
        - `country`: the name of the `country` where the job is located (case-insensitive)
        - `city`: the name of the `city` where the job is located (case-insensitive)
        - `fullTime`: whether the job is `full-time` (boolean)
        - `partTime`: whether the job is `part-time` (boolean)
        - `contract`: whether the job has a `contract` (boolean)
        - `timing`: the `working days` for the job (case-insensitive)
        - `salary`: the `budget amount` range for the job (inclusive)

    Note that not all criteria need to be provided for a query.

    Parameters:
        - `filters.FilterSet`: A Django FilterSet class used for filtering querysets.

    Returns:
        A filtered queryset of JobDetails based on the specified criteria.
    """

    country = filters.CharFilter(field_name='country__title', lookup_expr='iexact')
    city = filters.CharFilter(field_name='city__title', lookup_expr='iexact')
    fullTime = filters.BooleanFilter(field_name='is_full_time')
    partTime = filters.BooleanFilter(field_name='is_part_time')
    contract = filters.BooleanFilter(field_name='has_contract')
    timing = filters.CharFilter(field_name='duration', lookup_expr='iexact')
    salary = filters.RangeFilter(field_name='budget_amount', lookup_expr='iexact')
    class Meta:
        model = JobDetails
        fields = ['country', 'city', 'fullTime', 'partTime', 'contract', 'timing', 'salary']