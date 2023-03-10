from django.urls import path

from .views import (
    CountryView, CityView, JobCategoryView, 
    EducationLevelView, LanguageView, SkillView,
    TagView, ChangePasswordView, UserRightsView,
    PrivacyPolicyView, CandidatesListView, EmployerListView,
    JobsListView, UsersCountView, UserView,
    JobsRevertView, DashboardView
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
    
    path('/user-rights', UserRightsView.as_view(), name="user_rights"),
    
    path('/privacy-policy', PrivacyPolicyView.as_view(), name="privacy_policy"),
    
    path('/candidates', CandidatesListView.as_view(), name="candidates_list"),
    
    path('/employer', EmployerListView.as_view(), name="employer_list"),
    
    path('/user/<str:userId>', UserView.as_view(), name="user"),
    
    path('/jobs', JobsListView.as_view(), name="jobs_list"),
    path('/jobs/<str:jobId>', JobsListView.as_view(), name="jobs_list"),
    path('/jobs/<str:jobId>/revert', JobsRevertView.as_view(), name="jobs_rrevert"),
    
    path('/users-count', UsersCountView.as_view(), name="users_count"),
    
    path('/dashboard', DashboardView.as_view(), name="dashboard"),
]