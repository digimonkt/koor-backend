from django.urls import path

from .views import (
    UpdateAboutView, EducationsView, LanguageView,
    WorkExperiencesView, SkillsView, JobsApplyView,
    JobsSaveView, UpdateJobPreferencesView, AdditionalParameterView,
    CategoryView
)

app_name = "job_seekers"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),
    
    path('/educations', EducationsView.as_view(), name="educations"),
    path('/educations/<str:educationId>', EducationsView.as_view(), name="educations"),
    
    path('/language', LanguageView.as_view(), name="language"),
    path('/language/<str:languageId>', LanguageView.as_view(), name="language"),
    
    path('/work-experiences', WorkExperiencesView.as_view(), name="work_experiences"),
    path('/work-experiences/<str:workExperienceId>', WorkExperiencesView.as_view(), name="work_experiences"),
    
    path('/skills', SkillsView.as_view(), name="skills"),
    
    path('/jobs/apply', JobsApplyView.as_view(), name="jobs_apply"),
    path('/jobs/apply/<str:jobId>', JobsApplyView.as_view(), name="jobs_apply"),
    
    path('/jobs/save', JobsSaveView.as_view(), name="jobs_save"),
    path('/jobs/save/<str:jobId>', JobsSaveView.as_view(), name="jobs_save"),
    
    path('/job-preferences', UpdateJobPreferencesView.as_view(), name="update_job_preferences"),
    
    path('/additional-parameter', AdditionalParameterView.as_view(), name="additional_parameter"),
    
    path('/category', CategoryView.as_view(), name="category"),
]
