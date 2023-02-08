from django.urls import path

from .views import UserView, CreateSessionView, DeleteSessionView

app_name = "users"

urlpatterns = [

    path('', UserView.as_view(), name="get_user"),

    path('/session', CreateSessionView.as_view(), name="create_session"),
    
    path('/delete-session', DeleteSessionView.as_view(), name="delete_session"),
]
