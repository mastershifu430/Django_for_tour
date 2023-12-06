from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    # path("/booking", views.booking, name="booking"),
    path("season/", SeasonView.as_view(), name="season"),
    path("signup/", Signup.as_view(), name="signup"),
]
