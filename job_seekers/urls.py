from django.urls import path

from .views import UpdateAboutView, JobSearchView

app_name = "job_seekers"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/job-search', JobSearchView.as_view(), name="job_search"),

]
