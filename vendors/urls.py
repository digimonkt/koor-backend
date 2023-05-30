from django.urls import path

from .views import (
    UpdateAboutView, TenderSaveView, TenderApplyView,
    SectorView
)

app_name = "vendors"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/sector', SectorView.as_view(), name="sector"),
    
    path('/tender/save', TenderSaveView.as_view(), name="tender_save"),
    path('/tender/save/<str:tenderId>', TenderSaveView.as_view(), name="tender_save"),
    
    path('/tender/apply', TenderApplyView.as_view(), name="tender_apply"),
    path('/tender/apply/<str:tenderId>', TenderApplyView.as_view(), name="tender_apply"),

]
