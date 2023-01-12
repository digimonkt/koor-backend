# IMPORT SOME USEFUL PACKAGES.
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

# DEFINE URLS FOR USER PROFILE APPLICATION FUNCTION.
urlpatterns = [

    path('', views.UserRegistrationView.as_view(), name="user_registration_view_link"),

    path('/session', views.UserLoginView.as_view(), name="user_login_view_link"),

]