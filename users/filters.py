import django_filters as filters

from .models import User

class UsersFilter(filters.FilterSet):
    """A filter set for querying job details based on various criteria.

    This filter set allows for filtering job details based on the following criteria:
        - `country`: the name of the `country` where the job is located (case-insensitive)
        - `city`: the name of the `city` where the job is located (case-insensitive)
        - `timing`: the `working days` for the job (case-insensitive)
        - `salary`: the `budget amount` range for the job (inclusive)

    Note that not all criteria need to be provided for a query.

    Parameters:
        - `filters.FilterSet`: A Django FilterSet class used for filtering querysets.

    Returns:
        A filtered queryset of JobDetails based on the specified criteria.
    """

    country = filters.CharFilter(field_name='user_profile_jobseekerprofile_user__country__title', lookup_expr='iexact')
    city = filters.CharFilter(field_name='user_profile_jobseekerprofile_user__city__title', lookup_expr='iexact')
    experience = filters.NumberFilter(field_name='user_profile_jobseekerprofile_user__experience', lookup_expr='gte')
    availability = filters.BooleanFilter(field_name='job_seekers_jobpreferences_user__is_available')
    salary = filters.RangeFilter(field_name='job_seekers_jobpreferences_user__expected_salary', lookup_expr='iexact')
    vendor_country = filters.CharFilter(field_name='user_profile_vendorprofile_users__country__title', lookup_expr='iexact')
    vendor_city = filters.CharFilter(field_name='user_profile_vendorprofile_users__city__title', lookup_expr='iexact')
    years_in_market = filters.NumberFilter(field_name='user_profile_vendorprofile_users__operating_years', lookup_expr='gte')
    class Meta:
        model = User
        fields = [
            'country', 'city', 'experience', 'availability', 'salary', 
            'vendor_country', 'vendor_city', 'years_in_market'
        ]