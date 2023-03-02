from django.urls import path

from .views import (
    UserView, CreateSessionView, DeleteSessionView,
    DisplayImageView, ForgetPasswordView, ChangePasswordView
    )

app_name = "users"

urlpatterns = [

    path('', UserView.as_view(), name="get_user"),

    path('/session', CreateSessionView.as_view(), name="create_session"),
    
    path('/delete-session', DeleteSessionView.as_view(), name="delete_session"),
    
    path('/display-image', DisplayImageView.as_view(), name="display_image"),
    
    path('/forget-password', ForgetPasswordView.as_view(), name="forget_password"),
    
    path('/change-password/<str:otp>', ChangePasswordView.as_view(), name="change_password"),
]
