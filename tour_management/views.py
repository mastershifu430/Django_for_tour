import datetime
from django.shortcuts import render
from django.http import HttpResponse

from .models import Supplier, Booking


def index(request):
    return HttpResponse("Hello! Welcome! Hello world!")


def booking(request):
    if request.method == "POST":
        # Extract supplier ID from form data
        supplier_id = request.POST["supplier"]

        # Get the selected supplier
        supplier = Supplier.objects.get(pk=supplier_id)

        # Get tours for the selected supplier
        tours = Tour.objects.filter(supplier=supplier)

        # Filter tours based on booking date
        booking_date = datetime.now()
        available_tours = []
        for tour in tours:
            if (
                tour.availability["available_seats"] >= 1
                and booking_date >= tour.start_date
                and booking_date <= tour.end_date
            ):
                available_tours.append(tour)

        if request.POST["tour_package"]:
            # Extract tour package ID from form data if selected
            tour_package_id = request.POST["tour_package"]

            # Get the selected tour package
            tour_package = Tour.objects.get(pk=tour_package_id)

            # Create a new booking instance
            booking = Booking()
            booking.customer_name = request.POST["customer_name"]
            booking.customer_last_name = request.POST["customer_last_name"]
            booking.payer = request.POST["payer"]
            booking.tour = tour_package
            booking.booking_date = datetime.now()
            booking.number_of_guests = 1  # Assuming single booking
            booking.status = "Pending"
            booking.save()

            # Send booking confirmation email
            send_booking_confirmation_email(
                booking.customer_name, booking.customer_last_name, booking
            )

            # Redirect to booking confirmation page
            return render(request, "booking_confirmation.html", {"booking": booking})
        else:
            # Display booking form with available tours
            return render(
                request,
                "booking.html",
                {"suppliers": suppliers, "available_tours": available_tours},
            )
    else:
        # Display booking form with suppliers
        return render(request, "booking.html", {"suppliers": suppliers})
