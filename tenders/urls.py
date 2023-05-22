from django.urls import path

from .views import (
    TenderSearchView, TenderDetailView, TenderFilterView,
    TenderSuggestionView
)

app_name = "tenders"

urlpatterns = [

    path('', TenderSearchView.as_view(), name="tender_search"),
    
    path('/filter', TenderFilterView.as_view(), name="tender_filter"),
    path('/filter/<str:filterId>', TenderFilterView.as_view(), name="tender_filter"),
    
    path('/<str:tenderId>', TenderDetailView.as_view(), name="tender_detail"),
    path('/<str:tenderId>/suggestion', TenderSuggestionView.as_view(), name="tender_suggestion"),  

]
