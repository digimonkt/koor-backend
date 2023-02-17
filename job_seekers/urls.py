from django.urls import path

from .views import (
    UpdateAboutView, EducationsView, LanguageView
    )

app_name = "job_seekers"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/educations', EducationsView.as_view(), name="educations"),
    
    path('/educations/<str:educationId>', EducationsView.as_view(), name="educations"),
    
    path('/language', LanguageView.as_view(), name="language"),
    
]
