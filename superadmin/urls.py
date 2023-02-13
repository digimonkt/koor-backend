from django.urls import path

from .views import CountryView, CityView, JobCategoryView

app_name = "superadmin"

urlpatterns = [

    path('/country', CountryView.as_view(), name="country"),
    
    path('/city', CityView.as_view(), name="city"),
    
    path('/job-category', JobCategoryView.as_view(), name="job_category"),
    
]