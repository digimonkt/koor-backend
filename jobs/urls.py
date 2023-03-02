from django.urls import path

from .views import (
    JobSearchView, JobDetailView, JobApplicationsView,
    RecentApplicationsView, ApplicationsDetailView
)

app_name = "jobs"

urlpatterns = [

    path('', JobSearchView.as_view(), name="job_search"),
    path('/applications', RecentApplicationsView.as_view(), name="recent_applications"),
    path('/applications-detail/<str:applicationId>', ApplicationsDetailView.as_view(), name="applications_detail"),
    
    path('/<str:jobId>', JobDetailView.as_view(), name="job_detail"),    
    path('/<str:jobId>/applications', JobApplicationsView.as_view(), name="job_applications"),


]
