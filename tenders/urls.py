from django.urls import path

from .views import (
    TenderSearchView
)

app_name = "tenders"

urlpatterns = [

    path('', TenderSearchView.as_view(), name="tender_search"),

]
