from django.urls import path, include

app_name = "v1"

urlpatterns = [
    path('users', include('users.urls')),

    path('users/employer', include('employers.urls')),

    path('users/job-seeker', include('job_seekers.urls')),

    path('users/vendor', include('vendors.urls')),

    path('jobs', include('jobs.urls')),

    path('tenders', include('tenders.urls')),

    path('admin', include('superadmin.urls')),
    
    path('chat', include('chat.urls')),
]
