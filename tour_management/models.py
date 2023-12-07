from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Tourtype(models.TextChoices):
    AERIAL = "Aerial"
    ADVENTURE = "Adventure"
    AQUATIC = "Aquatic"
    COMBINED = "Combined"
    EXTREME = "Extreme"
    NIGHTOUT = "Nightout"
    SIGHTSEEING = "Sightseeing"
    TERRESTRIAL = "Terrestrial"


class Status(models.TextChoices):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELED = "canceled"
    REFUNDED = "refunded"


class CustomUser(models.Model):
    class Roles(models.TextChoices):
        ADMIN = "admin"
        SUB_ADMIN = "sub_admin"
        AGENCY = "agency"
        SUPPLIER = "supplier"
        REPRESENTATIVE = "representative"
        CUSTOMER = "customer"

    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    role = models.CharField(
        max_length=20, choices=Roles.choices, default=Roles.CUSTOMER
    )
    is_active = models.BooleanField(default=True)

    contact_information = models.JSONField(null=True)
    travel_preferences = models.JSONField(null=True)
    travel_history = models.TextField(null=True)
    prefered_language = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class OnlineUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


class Payer(models.TextChoices):
    DIRECT_CLIENT = "direct_client"
    AGENCY = "agency"


class Booking(models.Model):
    customer_name = models.CharField(max_length=20)
    customer_last_name = models.CharField(max_length=20)
    contact_information = models.JSONField()
    date_time = models.DateTimeField(default=timezone.now)
    payer = models.CharField(
        max_length=15, choices=Payer.choices, default=Payer.DIRECT_CLIENT
    )
    number_of_guests = models.IntegerField(default=0)
    tour_type = models.CharField(
        max_length=20, choices=Tourtype.choices, default=Tourtype.AERIAL
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )


class Pricing(models.Model):
    agency_rate = models.IntegerField(default=0)
    direct_customer_rate = models.IntegerField(default=0)
    supplier_cost = models.IntegerField(default=0)
    profit_margin = models.IntegerField(default=0)


class Supplier(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pricing = models.JSONField()


class TourPackage(models.Model):
    tour_name = models.CharField(max_length=255)
    description = models.TextField()
    itinerary = models.TextField()
    duration = models.IntegerField()
    included = models.TextField()
    excluded = models.TextField()
    remarks = models.TextField()
    pricing = models.JSONField()  # Pricing structure based on tour package and season
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    availability = models.JSONField()  # Availability by date, tour type, and supplier


class Season(models.Model):
    season_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()


class TourPackagePricing(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    price_tier = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    profit_margin_type = models.CharField(max_length=255)  # Percentage or fixed amount
    profit_margin_value = models.DecimalField(max_digits=10, decimal_places=2)


class TourSchedule(models.Model):
    date = models.DateField()
    tour_type = models.CharField(
        max_length=15, choices=Tourtype.choices, default=Tourtype.AERIAL
    )
    supplier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    guide_assigned = models.TextField()
    shift_details = models.TextField()
    payer = models.CharField(
        max_length=15, choices=Payer.choices, default=Payer.DIRECT_CLIENT
    )


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_messages"
    )
    message_content = models.TextField()
    payer = models.CharField(
        max_length=15, choices=Payer.choices, default=Payer.DIRECT_CLIENT
    )


class PaymentInfo(models.Model):
    method = models.TextField()
    status = models.TextField()


class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    information = models.TextField()
    special_request = models.TextField()


class CommissionAgreement(models.Model):
    commission_rate = models.IntegerField()
    payment_terms = models.TextField()


class Shift(models.Model):
    class ShiftOption(models.TextChoices):
        MORNING = "morning"
        AFTERNOON = "afternoon"
        NIGHT = "night"

    date = models.DateField()
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    shift_time = models.DateTimeField()
    shift_option = models.CharField(
        max_length=15, choices=ShiftOption.choices, default=ShiftOption.MORNING
    )


class GuideAvailability(models.Model):
    date_time = models.DateTimeField()
    preferred_language = models.TextField()


class Setting(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    interface_language = models.TextField()
    pickup_list = models.JSONField()


class Reports(models.Model):
    class ReportsType(models.TextChoices):
        BOOKING = "booking"
        SALES = "sales"
        CUSTOMER_ACTIVITY = "customer_activity"
        SUPPLIER_PERFORMANCE = "supplier_performance"

    report_type = models.CharField(
        max_length=20, choices=ReportsType.choices, default=ReportsType.BOOKING
    )


class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.IntegerField()
    history = models.JSONField()
