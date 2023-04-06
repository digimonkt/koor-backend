from django.urls import path

from .views import (
    TenderSearchView, TenderDetailView
)

app_name = "tenders"

urlpatterns = [

    path('', TenderSearchView.as_view(), name="tender_search"),
    
    path('/<str:tenderId>', TenderDetailView.as_view(), name="tender_detail"),    

]
