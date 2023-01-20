# IMPORT SOME USEFUL PACKAGES.
from django.urls import path
# IMPORT SOME USEFUL VIEWS FILE.
from . import views

# DEFINE URLS FOR USER PROFILE APPLICATION FUNCTION.
urlpatterns = [

    path('', views.UserRegistrationView.as_view(), name="user_registration_view_link"),


]