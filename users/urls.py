# IMPORT SOME USEFUL PACKAGES.
from django.urls import path

from . import views

from django.views.decorators.csrf import csrf_exempt

# DEFINE URLS FOR USER PROFILE APPLICATION FUNCTION.
urlpatterns = [

    path('', views.UserRegistrationView.as_view(), name="user_registration_view_link"),

    path('/session', views.UserLoginView.as_view(), name="user_login_view_link"),

    path('/delete-session', views.UserLogoutView.as_view(), name="user_logout_view_link"),

    path('/detail', views.UserDetailView.as_view(), name="user_detail_view_link"),

]