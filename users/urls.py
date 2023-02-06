from django.urls import path

from .views import CreateUserView, CreateSessionView

app_name = "users"

urlpatterns = [
    path('', CreateUserView.as_view(), name="create_user"),

    path('/session', CreateSessionView.as_view(), name="create_session")
]
