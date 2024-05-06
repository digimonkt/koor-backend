from django.urls import path

from .views import (
    UpdateAboutView, JobsView,
    TendersView, JobsStatusView, JobApplicationView,
    TendersStatusView, ActivityView,
    JobAnalysisView, BlacklistedUserView,
    ShareCountView, ActiveJobsView, UnblockUserView,
    TenderApplicationView, ActiveTendersView
)

app_name = "employers"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/activity', ActivityView.as_view(), name="activity"),
    path('/job-analysis', JobAnalysisView.as_view(), name="job_analysis"),
    path('/share-count', ShareCountView.as_view(), name="share_count"),
    
    path('/jobs', JobsView.as_view(), name="jobs"), 
    path('/jobs/<str:jobId>', JobsView.as_view(), name="jobs"),
    path('/jobs/<str:jobId>/status', JobsStatusView.as_view(), name="jobs_status"),
    
    path('/tenders', TendersView.as_view(), name="tenders"),
    path('/tenders/<str:tendersId>', TendersView.as_view(), name="tenders"),
    path('/tenders/<str:tendersId>/status', TendersStatusView.as_view(), name="Tenders_status"),
    
    path('/blacklisted-user', BlacklistedUserView.as_view(), name="blacklisted_user"), 
    path('/unblock-user/<str:userId>', UnblockUserView.as_view(), name="unblock_user"), 
    
    path('/active-jobs/<str:employerId>', ActiveJobsView.as_view(), name="active_jobs"), 
    path('/active-tenders/<str:employerId>', ActiveTendersView.as_view(), name="active_tenders"), 
    
    path('/job-application/<str:jobSeekerId>', JobApplicationView.as_view(), name="job_application"), 
    path('/tender-application/<str:vendorId>', TenderApplicationView.as_view(), name="tender_application"), 
]
