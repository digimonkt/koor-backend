import django_filters as filters

from .models import RechargeHistory

class RechargeHistoryDetailsFilter(filters.FilterSet):

    employer = filters.CharFilter(field_name='user__id', lookup_expr='iexact')
    sent = filters.CharFilter(field_name='is_send', lookup_expr='iexact')
    
    class Meta:
        model = RechargeHistory
        fields = ['employer', 'sent']