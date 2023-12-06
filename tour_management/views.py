import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import HttpResponse

from .models import *
from .serializers import *


def index(request):
    return Response({"message": "Hello world!"})


# def booking(request):
#     if request.method == "POST":
#         # Extract supplier ID from form data
#         supplier_id = request.POST["supplier"]

#         # Get the selected supplier
#         supplier = Supplier.objects.get(pk=supplier_id)

#         # Get tours for the selected supplier
#         tours = TourPackage.objects.filter(supplier=supplier)

#         # Filter tours based on booking date
#         booking_date = datetime.now()
#         available_tours = []
#         for tour in tours:
#             if (
#                 tour.availability["available_seats"] >= 1
#                 and booking_date >= tour.start_date
#                 and booking_date <= tour.end_date
#             ):
#                 available_tours.append(tour)

#         if request.POST["tour_package"]:
#             # Extract tour package ID from form data if selected
#             tour_package_id = request.POST["tour_package"]

#             # Get the selected tour package
#             tour_package = TourPackage.objects.get(pk=tour_package_id)

#             # Create a new booking instance
#             booking = Booking()
#             booking.customer_name = request.POST["customer_name"]
#             booking.customer_last_name = request.POST["customer_last_name"]
#             booking.payer = request.POST["payer"]
#             booking.tour = tour_package
#             booking.booking_date = datetime.now()
#             booking.number_of_guests = 1  # Assuming single booking
#             booking.status = "Pending"
#             booking.save()

#             # Send booking confirmation email
#             # send_booking_confirmation_email(
#             #     booking.customer_name, booking.customer_last_name, booking
#             # )

#             # Redirect to booking confirmation page
#             return render(request, "booking_confirmation.html", {"booking": booking})
#         else:
#             # Display booking form with available tours
#             return render(
#                 request,
#                 "booking.html",
#                 {"suppliers": suppliers, "available_tours": available_tours},
#             )
#     else:
#         # Display booking form with suppliers
#         return render(request, "booking.html", {"suppliers": suppliers})


class SeasonView(APIView):
    model = Season
    serializer_class = SeasonSerializer

    def get(self, request, *arg, **kwargs):
        seasons = self.model.objects.all()
        serializers = self.serializer_class(seasons, many=True).data
        if request.query_params.get("id", None) is not None:
            season = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(season).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(serializers, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if request.query_params.get("id", None) is not None:
            try:
                season = self.model.objects.get(id=request.query_params.get("id"))
            except self.model.DoesNotExist:
                return Response({"success": False}, status=HTTP_400_BAD_REQUEST)
            season.delete()
            return Response({"success": True})
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)

    def post(self, request, *arg, **kwargs):
        if request.query_params.get("id", None) is not None:
            season = self.model.objects.get(id=request.query_params.get("id"))
            if request.data.get("season_name", None) is not None:
                season.season_name = request.data.get("season_name")
            if request.data.get("start_date", None) is not None:
                season.start_date = request.data.get("start_date")
            if request.data.get("end_date", None) is not None:
                season.end_date = request.data.get("end_date")
            season.save()
            return Response({"success": True})

        seasonserializer = self.serializer_class(data=request.data)
        if seasonserializer.is_valid():
            season = self.model.objects.create(**seasonserializer.validated_data)
            season.save()
            return Response({"success": True, "season": seasonserializer.data})


class Signup(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            role = serializer.data.get("role")
            if role == "admin":
                user = get_user_model().objects.create_super_user(
                    **serializer.validated_data
                )
                user.save()
            else:
                user = get_user_model().objects.create_user(**serializer.validated_data)
                user.save()
                if role == "suppiler":
                    Supplier.objects.create(user=user)
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)
