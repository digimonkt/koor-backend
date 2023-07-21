import django_filters as filters

from .models import PointInvoice

class PointInvoiceDetailsFilter(filters.FilterSet):

    invoice_id = filters.CharFilter(field_name='invoice_id', lookup_expr='iexact')
    employer = filters.CharFilter(field_name='user__id', lookup_expr='iexact')
    sent = filters.CharFilter(field_name='is_send', lookup_expr='iexact')
    
    class Meta:
        model = PointInvoice
        fields = ['invoice_id', 'employer', 'sent']