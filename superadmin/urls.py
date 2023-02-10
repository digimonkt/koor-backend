from django.urls import path

from .views import CountryView, CityView

app_name = "superadmin"

urlpatterns = [

    path('/country', CountryView.as_view(), name="country"),
    
    path('/city', CityView.as_view(), name="city"),
    
]