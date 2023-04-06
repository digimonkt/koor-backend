from django.urls import path

from .views import (
    UpdateAboutView
)

app_name = "vendors"

urlpatterns = [

    path('/about-me', UpdateAboutView.as_view(), name="update_about"),

]
