from django.urls import path

from .views import (
    TenderSearchView, TenderDetailView, TenderFilterView,
    TenderSuggestionView, ApplicationsDetailView,
    TenderApplicationsView, RecentApplicationsView
)

app_name = "tenders"

urlpatterns = [

    path('', TenderSearchView.as_view(), name="tender_search"),
    
    path('/applications', RecentApplicationsView.as_view(), name="recent_applications"),
    
    path('/filter', TenderFilterView.as_view(), name="tender_filter"),
    path('/filter/<str:filterId>', TenderFilterView.as_view(), name="tender_filter"),
    
    path('/applications-detail/<str:applicationId>', ApplicationsDetailView.as_view(), name="applications_detail"),
    
    path('/<str:tenderId>', TenderDetailView.as_view(), name="tender_detail"),
    path('/<str:tenderId>/applications', TenderApplicationsView.as_view(), name="tender_applications"),
    path('/<str:tenderId>/suggestion', TenderSuggestionView.as_view(), name="tender_suggestion"),  

]
