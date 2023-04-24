from django.urls import path

from .views import (
    UpdateAboutView, JobsView,
    TendersView, JobsStatusView,
    TendersStatusView, ActivityView,
    JobAnalysisView, BlacklistedUserView
)

app_name = "employers"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/activity', ActivityView.as_view(), name="activity"),
    path('/job-analysis', JobAnalysisView.as_view(), name="job_analysis"),
    
    path('/jobs', JobsView.as_view(), name="jobs"), 
    path('/jobs/<str:jobId>', JobsView.as_view(), name="jobs"),
    path('/jobs/<str:jobId>/status', JobsStatusView.as_view(), name="jobs_status"),
    
    path('/tenders', TendersView.as_view(), name="tenders"),
    path('/tenders/<str:tendersId>', TendersView.as_view(), name="tenders"),
    path('/tenders/<str:tendersId>/status', TendersStatusView.as_view(), name="Tenders_status"),
    
    path('/blacklisted-user', BlacklistedUserView.as_view(), name="blacklisted_user"), 
]
