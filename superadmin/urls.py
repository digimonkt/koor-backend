from django.urls import path

from .views import (
    CountryView, CityView, JobCategoryView, 
    EducationLevelView, LanguageView, SkillView
    )

app_name = "superadmin"

urlpatterns = [

    path('/country', CountryView.as_view(), name="country"),
    path('/country/<str:countryId>', CountryView.as_view(), name="country"),
    
    path('/city', CityView.as_view(), name="city"),
    path('/city/<str:cityId>', CityView.as_view(), name="city"),
    
    path('/job-category', JobCategoryView.as_view(), name="job_category"),
    
    path('/education-level', EducationLevelView.as_view(), name="education_level"),
    
    path('/language', LanguageView.as_view(), name="language"),
    
    path('/skills', SkillView.as_view(), name="skills"),
    
]