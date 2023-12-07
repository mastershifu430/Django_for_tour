import datetime
import django.db
from django.shortcuts import render
import rest_framework
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
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class Signup(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create(**serializer.validated_data)
            user.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class BookingView(APIView):
    model = Booking
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        bookings = self.model.objects.all()
        serializers = self.serializer_class(bookings, many=True).data
        if request.query_params.get("id", None) is not None:
            booking = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(booking).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(serializers, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if request.query_params.get("id", None) is not None:
            booking = self.model.objects.get(id=request.query_params.get("id"))
            if request.data.get("status", None) is not None:
                booking.status = request.data.get("status")
            if request.data.get("tour_type", None) is not None:
                booking.tour_type = request.data.get("tour_type")
            if request.data.get("number_of_guests", None) is not None:
                booking.number_of_guests = request.data.get("number_of_guests")
            if request.data.get("date_time", None) is not None:
                booking.date_time = request.data.get("date_time")
            if request.data.get("contact_infomation", None) is not None:
                booking.contact_infomation = request.data.get("contact_infomation")
            booking.save()
            return Response({"success": True})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            booking = self.model.objects.create(**serializer.validated_data)
            booking.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class MessageView(APIView):
    model = Message
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        messages = self.model.objects.all()
        serializers = self.serializer_class(messages, many=True).data
        if request.query_params.get("id", None) is not None:
            message = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(message).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(serializers, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if request.query_params.get("id", None) is not None:
            try:
                message = self.model.objects.get(id=request.query_params.get("id"))
            except self.model.DoesNotExist:
                return Response({"success": False}, status=HTTP_400_BAD_REQUEST)
            message.delete()
            return Response({"success": True})
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        messageserializer = self.serializer_class(data=request.data)
        if messageserializer.is_valid():
            message = self.model.objects.create(**messageserializer.validated_data)
            message.save()
            return Response({"success": True, "message": messageserializer.data})
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class ClientView(APIView):
    model = Client
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        clients = self.model.objects.all()
        serializers = self.serializer_class(clients, many=True).data
        if request.query_params.get("id", None) is not None:
            client = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(client).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(serializers, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            client = self.model.create(**serializer.validated_data)
            client.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class TourPackageView(APIView):
    model = TourPackage
    serializer_class = TourPackageSerializer

    def get(self, request, *args, **kwargs):
        tourpackages = self.model.objects.all()
        serializers = self.serializer_class(tourpackages, many=True).data
        if request.query_params.get("id", None) is not None:
            tourpackage = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(tourpackage).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(serializers, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            tourpackage = self.model.create(**serializer.validated_data)
            tourpackage.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class SupplierView(APIView):
    model = Supplier
    serializer_class = SupplierSerializer

    def get(self, request, *args, **kwargs):
        suppilers = self.model.objects.all()
        serializers = self.serializer_class(suppilers, many=True).data
        if request.query_params.get("id", None) is not None:
            supplier = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(supplier).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(serializers, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            supplier = self.model.create(**serializer.validated_data)
            supplier.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)


class ShiftView(APIView):
    model = Shift
    serializer_class = ShiftSerializer

    def get(self, request, *args, **kwargs):
        shifts = self.model.objects.all()
        serializers = self.serializer_class(shifts, many=True).data
        if request.query_params.get("id", None) is not None:
            shift = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(shift).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(serializers, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            shift = self.model.create(**serializer.validated_data)
            shift.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)
    
class SettingView(APIView):
    model = Setting
    serializer_class = SettingSerializer
    
    def get(self, request, *args, **kwargs):
        if request.query_params.get("id", None) is not None:
            setting = self.model.objects.get(id=request.query_params.get("id"))
            serializer = self.serializer_class(setting).data
            return Response(serializer, status=HTTP_200_OK)
    
    def post(self, request, *arg, **kwargs):
        if request.query_params.get("id", None) is not None:
            setting = self.model.objects.get(id=request.query_params.get("id"))
            if request.data.get("user", None) is not None:
                setting.user = request.data.get("user")
            if request.data.get("interface_language", None) is not None:
                setting.interface_language = request.data.get("interface_language")
            if request.data.get("pickup_list", None) is not None:
                setting.pickup_list = request.data.get("pickup_list")
            setting.save()
            return Response({"success": True})

        seasonserializer = self.serializer_class(data=request.data)
        if seasonserializer.is_valid():
            setting = self.model.objects.create(**seasonserializer.validated_data)
            setting.save()
            return Response({"success": True}, status=HTTP_200_OK)
        return Response({"success": False}, status=HTTP_400_BAD_REQUEST)