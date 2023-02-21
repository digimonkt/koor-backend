from django.urls import path

from .views import (
    JobSearchView, JobDetailView, JobApplicationsView,
    RecentApplicationsView
)

app_name = "jobs"

urlpatterns = [

    path('', JobSearchView.as_view(), name="job_search"),
    path('/applications', RecentApplicationsView.as_view(), name="recent_applications"),
    
    path('/<str:jobId>', JobDetailView.as_view(), name="job_detail"),    
    path('/applications/<str:jobId>', JobApplicationsView.as_view(), name="job_applications"),


]
