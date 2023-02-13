from django.urls import path

from .views import UpdateAboutView, CreateJobsView

app_name = "employers"

urlpatterns = [

    path('', UpdateAboutView.as_view(), name="update_about"),
    
    path('/jobs', CreateJobsView.as_view(), name="create_jobs")
    
]
