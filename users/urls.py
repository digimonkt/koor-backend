from django.urls import path

from .views import CreateUserView, CreateSessionView

app_name = "users"

urlpatterns = [
    path('', CreateUserView.as_view(), name="create_user"),

<<<<<<< HEAD
    path('', views.CreateUserView.as_view(), name="create_user_view_link"),

    path('/session', views.CreateSessionView.as_view(), name="create_session_view_link"),

    path('/delete-session', views.DeleteSessionView.as_view(), name="delete_session_view_link"),

=======
    path('/session', CreateSessionView.as_view(), name="create_session")
>>>>>>> b6c4e2cff68ff6f1a5f87b6fafc46e529900c624
]
