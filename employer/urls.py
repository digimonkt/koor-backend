# IMPORT SOME USEFUL PACKAGES.
from django.urls import path

# IMPORT SOME USEFUL VIEWS FILE.
from . import views

# DEFINE URLS FOR USER PROFILE APPLICATION FUNCTION.
urlpatterns = [

    path('/about-me', views.UpdateEmployerAboutView.as_view(), name="update_employer_about_view_link"),

]
