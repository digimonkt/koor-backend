from django.urls import path

from .views import UpdateAboutView

app_name = "job_seekers"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),

]
