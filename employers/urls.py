from django.urls import path

from .views import UpdateAboutView, JobsView

app_name = "employers"

urlpatterns = [

    path('', UpdateAboutView.as_view(), name="update_about"),
    
    path('/jobs', JobsView.as_view(), name="jobs")
    
]
