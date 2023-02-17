from django.urls import path

from .views import (
    JobSearchView, JobDetailView
)

app_name = "jobs"

urlpatterns = [

    path('', JobSearchView.as_view(), name="job_search"),
    
    path('/<str:jobId>', JobDetailView.as_view(), name="job_detail"),

]
