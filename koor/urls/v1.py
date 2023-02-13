from django.urls import path, include

app_name="v1"

urlpatterns = [
    path('users', include('users.urls')),
    
    path('users/employer', include('employers.urls')),
    
    path('admin', include('superadmin.urls')),
]