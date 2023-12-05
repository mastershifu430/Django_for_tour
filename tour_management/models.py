from django.db import models

# Create your models here.


class Booking(models.Model):
    customer_name = models.CharField(max_length=20)
    customer_last_name = models.CharField(max_length=20)
    contact_information = models.JSONField()
    time = models.DateTimeField()
    payer = models.CharField(
        max_length=15,
        choices=[("direct_client", "Direct Client"), ("agency", "Agency")],
    )
    number_of_guests = models.IntegerField()
    tour_type = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("canceled", "Canceled"),
            ("refunded", "Refunded"),
        ],
    )


class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_information = models.JSONField()
    travel_preferences = models.JSONField()
    travel_history = models.TextField()
    preferred_language = models.CharField(max_length=255)


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    contact_person_last_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    contact_information = models.JSONField()
    preferred_languages = models.CharField(max_length=255)


class TourPackage(models.Model):
    tour_name = models.CharField(max_length=255)
    description = models.TextField()
    itinerary = models.TextField()
    duration = models.IntegerField()
    included = models.TextField()
    excluded = models.TextField()
    remarks = models.TextField()
    pricing = models.JSONField()  # Pricing structure based on tour package and season
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE)
    availability = models.JSONField()  # Availability by date, tour type, and supplier


class Season(models.Model):
    season_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()


class TourPackagePricing(models.Model):
    tour_package = models.ForeignKey("TourPackage", on_delete=models.CASCADE)
    season = models.ForeignKey("Season", on_delete=models.CASCADE)
    price_tier = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    profit_margin_type = models.CharField(max_length=255)  # Percentage or fixed amount
    profit_margin_value = models.DecimalField(max_digits=10, decimal_places=2)


class Tour(models.Model):
    tour_name = models.CharField(max_length=50)
    description = models.CharField()
    itinerary = models.CharField()
