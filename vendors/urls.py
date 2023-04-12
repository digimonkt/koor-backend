from django.urls import path

from .views import (
    UpdateAboutView, TenderSaveView
)

app_name = "vendors"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/tender/save', TenderSaveView.as_view(), name="tender_save"),
    path('/tender/save/<str:tenderId>', TenderSaveView.as_view(), name="tender_save"),

]
