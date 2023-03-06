from django.urls import path

from .views import (
    CountryView, CityView, JobCategoryView, 
    EducationLevelView, LanguageView, SkillView,
    TagView, ChangePasswordView
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
    path('/language/<str:languageId>', LanguageView.as_view(), name="language"),
    
    path('/skills', SkillView.as_view(), name="skills"),
    path('/skills/<str:skillId>', SkillView.as_view(), name="skills"),
    
    path('/tag', TagView.as_view(), name="tag"),
    path('/tag/<str:tagId>', TagView.as_view(), name="tag"),
    
    path('/change-password', ChangePasswordView.as_view(), name="change_password"),
]