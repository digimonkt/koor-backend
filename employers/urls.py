from django.urls import path

from .views import UpdateAboutView

app_name = "employers"

urlpatterns = [

    path('', UpdateAboutView.as_view(), name="update_about"),
    
]
