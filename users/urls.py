from django.urls import path

from .views import UserView, CreateSessionView

app_name = "users"

urlpatterns = [

    path('', UserView.as_view(), name="get_user"),

    path('/session', CreateSessionView.as_view(), name="create_session")
]
