from django.urls import path

from .views import CountryView

app_name = "superadmin"

urlpatterns = [

    path('/country', CountryView.as_view(), name="country"),
    
]