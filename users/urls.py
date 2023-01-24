# IMPORT SOME USEFUL PACKAGES.
from django.urls import path

# IMPORT SOME USEFUL VIEWS FILE.
from . import views

# DEFINE URLS FOR USER PROFILE APPLICATION FUNCTION.
urlpatterns = [

    path('', views.CreateUserView.as_view(), name="create_user_view_link"),

    path('session/', views.CreateSessionView.as_view(), name="create_session_view_link"),

]
