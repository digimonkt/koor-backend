from django.urls import path

from notification.views import NotificationView, NotificationSettingsView
from .views import (
    UserView, CreateSessionView, DeleteSessionView,
    DisplayImageView, SendOtpView, ChangePasswordView,
    GetLocationView, SocialLoginView, OtpVerificationView,
    VerificationView, SearchView, UserFilterView,
    VisitorLogView
    )

app_name = "users"

urlpatterns = [

    path('', UserView.as_view(), name="get_user"),
    
    path('/social-login', SocialLoginView.as_view(), name="social_login"),

    path('/session', CreateSessionView.as_view(), name="create_session"),
    
    path('/delete-session', DeleteSessionView.as_view(), name="delete_session"),
    
    path('/display-image', DisplayImageView.as_view(), name="display_image"),
    
    path('/send-otp', SendOtpView.as_view(), name="send_otp"),
    
    path('/otp-verification/<str:otp>', OtpVerificationView.as_view(), name="otp_verification"),
    
    path('/change-password', ChangePasswordView.as_view(), name="change_password"),
    
    path('/get-location', GetLocationView.as_view(), name="get_location"),
    
    path('/notification', NotificationView.as_view(), name="get_notification"),
    path('/notification/settings/<str:notificationType>', NotificationSettingsView.as_view(), name="notification_settings"),
    
    path('/email-verification/<str:otp>', VerificationView.as_view(), name="verification"),
    
    path('/search/<str:role>', SearchView.as_view(), name="search"),
    
    path('/filter', UserFilterView.as_view(), name="user_filter"),
    path('/filter/<str:filterId>', UserFilterView.as_view(), name="user_filter"),
    
    path('/visitor-log', VisitorLogView.as_view(), name="visitor_log"),
]
