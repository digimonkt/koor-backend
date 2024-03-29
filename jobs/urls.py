from django.urls import path

from .views import (
    JobSearchView, JobDetailView, JobApplicationsView,
    RecentApplicationsView, ApplicationsDetailView, JobSuggestionView,
    JobFilterView, JobShareView, JobCategoryView,
    PopularJobCategoryView, DownloadImage
)

app_name = "jobs"

urlpatterns = [

    path('', JobSearchView.as_view(), name="job_search"),
    
    path('/download-image', DownloadImage.as_view(), name='download_image'),
    
    path('/applications', RecentApplicationsView.as_view(), name="recent_applications"),
    
    path('/filter', JobFilterView.as_view(), name="job_filter"),
    path('/filter/<str:filterId>', JobFilterView.as_view(), name="job_filter"),
            
    path('/categories', JobCategoryView.as_view(), name="job_category"),
    path('/job-categories', PopularJobCategoryView.as_view(), name="popular_job_category"),
    
    path('/applications-detail/<str:applicationId>', ApplicationsDetailView.as_view(), name="applications_detail"),
    path('/applications-detail/<str:applicationId>/<str:action>', ApplicationsDetailView.as_view(), name="applications_detail"),
    
    path('/<str:jobId>', JobDetailView.as_view(), name="job_detail"),    
    path('/<str:jobId>/applications', JobApplicationsView.as_view(), name="job_applications"),
    path('/<str:jobId>/suggestion', JobSuggestionView.as_view(), name="job_suggestion"),
    
    path('/<str:jobId>/share', JobShareView.as_view(), name="job_share"),
    path('/<str:jobId>/share/<str:platform>', JobShareView.as_view(), name="job_share"),

]
