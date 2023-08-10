import django_filters as filters

from .models import Invoice

   
class InvoiceDetailsFilter(filters.FilterSet):
    """
    A FilterSet for filtering Invoice objects based on various criteria.

    This class defines filters that can be applied to the Invoice model to retrieve specific sets of invoices based on
    the employer and sent status.

    Filters:
    - employer (CharFilter): Filters invoices by the ID of the associated user (employer).
      This filter performs a case-insensitive exact match lookup on the 'user__id' field.

    - sent (CharFilter): Filters invoices by the 'is_send' status.
      This filter performs a case-insensitive exact match lookup on the 'is_send' field.

    Usage example:
    ```
    filter_set = InvoiceDetailsFilter(data={'employer': 'user123', 'sent': 'true'})
    queryset = filter_set.qs
    ```

    Attributes:
        employer (filters.CharFilter): A filter for the employer's user ID.
        sent (filters.CharFilter): A filter for the 'is_send' status.

    Meta:
        model (Invoice): The model class that this FilterSet is based on.
        fields (list): The list of fields available for filtering in this FilterSet.
    """

    employer = filters.CharFilter(field_name='user__id', lookup_expr='iexact')
    sent = filters.CharFilter(field_name='is_send', lookup_expr='iexact')
    
    class Meta:
        model = Invoice
        fields = ['employer', 'sent']
