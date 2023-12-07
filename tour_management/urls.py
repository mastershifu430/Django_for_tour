from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("season/", SeasonView.as_view(), name="season"),
    path("signup/", Signup.as_view(), name="signup"),
    path("booking/", BookingView.as_view(), name="booking"),
    path("message/", MessageView.as_view(), name="message"),
    path("client/", ClientView.as_view(), name="client"),
    path("tourpackage/", TourPackageView.as_view(), name="tourpackage"),
    path("shift/", ShiftView.as_view(), name="shift"),
    path("setting/", SettingView.as_view(), name="setting"),
]
