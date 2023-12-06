from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


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


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin"
        SUB_ADMIN = "sub_admin"
        AGENCY = "agency"
        SUPPLIER = "supplier"
        REPRESENTATIVE = "representative"
        CUSTOMER = "customer"

    username = None
    name = models.CharField(max_length=40, null=True)
    email = models.EmailField(_("Email address"), unique=True)
    role = models.CharField(max_length=8, choices=Roles.choices, default=Roles.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    contact_information = models.JSONField()
    travel_preferences = models.JSONField()
    travel_history = models.TextField()
    preferred_language = models.CharField(max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

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
    date_time = models.DateTimeField()
    payer = models.CharField(
        max_length=15, choices=Payer.choices, default=Payer.DIRECT_CLIENT
    )
    number_of_guests = models.IntegerField()
    tour_type = models.CharField(
        max_length=20, choices=Tourtype.choices, default=Tourtype.AERIAL
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )


class TourPackage(models.Model):
    tour_name = models.CharField(max_length=255)
    description = models.TextField()
    itinerary = models.TextField()
    duration = models.IntegerField()
    included = models.TextField()
    excluded = models.TextField()
    remarks = models.TextField()
    pricing = models.JSONField()  # Pricing structure based on tour package and season
    supplier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_content = models.TextField()
    payer = models.CharField(
        max_length=15, choices=Payer.choices, default=Payer.DIRECT_CLIENT
    )


class Pricing(models.Model):
    agency_rate = models.IntegerField()
    direct_customer_rate = models.IntegerField()
    supplier_cost = models.IntegerField()
    profit_margin = models.IntegerField()


class PaymentInfo(models.Model):
    method = models.TextField()
    status = models.TextField()


class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    information = models.TextField()
    special_request = models.TextField()


class Supplier(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)


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
