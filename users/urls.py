from django.urls import path

from notification.views import NotificationView, NotificationSettingsView, GetNotificationSettingsView
from .views import (
    UserView, CreateSessionView, DeleteSessionView,
    DisplayImageView, SendOtpView, ChangePasswordView,
    GetLocationView, SocialLoginView, OtpVerificationView,
    VerificationView, SearchView, UserFilterView,
    VisitorLogView, AnalyticView, VisitorsView,
    AccountVerificationView, ResendVerificationView
    )

app_name = "users"

urlpatterns = [

    path('', UserView.as_view(), name="get_user"),
    
    path('/social-login', SocialLoginView.as_view(), name="social_login"),
    path('/account-verification/<str:hash_code>', AccountVerificationView.as_view(), name="account_verification"),
    path('/resend-verification', ResendVerificationView.as_view(), name="resend_verification"),

    path('/session', CreateSessionView.as_view(), name="create_session"),
    
    path('/delete-session', DeleteSessionView.as_view(), name="delete_session"),
    
    path('/display-image', DisplayImageView.as_view(), name="display_image"),
    
    path('/send-otp', SendOtpView.as_view(), name="send_otp"),
    
    path('/otp-verification/<str:otp>', OtpVerificationView.as_view(), name="otp_verification"),
    
    path('/change-password', ChangePasswordView.as_view(), name="change_password"),
    
    path('/get-location', GetLocationView.as_view(), name="get_location"),
    
    path('/notification', NotificationView.as_view(), name="get_notification"),
    path('/notification/settings', GetNotificationSettingsView.as_view(), name="get_notification_settings"),
    path('/notification/settings/<str:notificationType>', NotificationSettingsView.as_view(), name="notification_settings"),
    path('/notification/<str:notificationId>', NotificationView.as_view(), name="get_notification"),
    path('/email-verification/<str:otp>', VerificationView.as_view(), name="verification"),
    
    path('/search/<str:role>', SearchView.as_view(), name="search"),
    
    path('/filter', UserFilterView.as_view(), name="user_filter"),
    path('/filter/<str:filterId>', UserFilterView.as_view(), name="user_filter"),
    
    path('/visitor-log', VisitorLogView.as_view(), name="visitor_log"),
    
    path('/analytic', AnalyticView.as_view(), name="analytic"),
    
    path('/visitors', VisitorsView.as_view(), name="visitors"),
]
