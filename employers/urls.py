from django.urls import path

from .views import UpdateAboutView, JobsView, TendersView

app_name = "employers"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/jobs', JobsView.as_view(), name="jobs"), 
    
    path('/jobs/<str:jobId>', JobsView.as_view(), name="jobs"),
    
    path('/tenders', TendersView.as_view(), name="tenders"),
    
]
