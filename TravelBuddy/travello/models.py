from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.
class Packages(models.Model):

    class Meta:
        verbose_name_plural = "Packages"

    location_id = models.CharField(max_length=15, primary_key=True)
    from_location = models.CharField(max_length=100, default="Bangalore")
    location_name = models.CharField(max_length=50)
    sub_title = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    days = models.IntegerField()
    date = models.DateField()
    total_number_seats = models.IntegerField()
    destination_image = models.ImageField(upload_to='destinations')


class VehicleAndGeneralDetails(models.Model):

    class Meta:
        verbose_name_plural = "Vehicle and general details"

    location_id = models.ForeignKey(Packages, on_delete=models.CASCADE, primary_key=True)
    vehicle_company_name = models.CharField(max_length=50)
    vehicle_model_number = models.CharField(max_length=20, blank=True, default=None)
    travel_starts_on = models.DateField(editable=False)
    reporting_time = models.TimeField(editable=False)
    reporting_location = models.TextField()
    departure_time = models.TimeField()
    departure_location = models.TextField()


class DestinationDetails(models.Model):

    class Meta:
        verbose_name_plural = "Destination details"

    place_id = models.CharField(max_length=25, primary_key=True)
    location_id = models.ForeignKey(Packages, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=50)
    visiting_on = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    place_image = models.ImageField(upload_to='places')


class PackagesGuide(models.Model):

    class Meta:
        verbose_name_plural = "Package guide"

    guide_id = models.CharField(max_length=25, primary_key=True)
    location_id = models.ForeignKey(Packages, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='guides')
    guide_name = models.CharField(max_length=20)
    age = models.IntegerField()
    experience = models.IntegerField()


class PackagesHotel(models.Model):

    class Meta:
        verbose_name_plural = "Package hotels"

    hotel_id = models.CharField(max_length=35, primary_key=True)
    location_id = models.ForeignKey(Packages, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=20)
    room_capacity = models.IntegerField()


class HotelImages(models.Model):

    class Meta:
        verbose_name_plural = "Hotel images"

    hotel_image = models.ImageField(upload_to='hotels')
    hotel_id = models.ForeignKey(PackagesHotel, on_delete=models.CASCADE)


class PackagesBookings(models.Model):

    class Meta:
        verbose_name_plural = "Booking details"

    booking_id = models.CharField(max_length=150, primary_key=True)
    location_id = models.ForeignKey(Packages, on_delete=models.CASCADE)
    username = models.ForeignKey(User, max_length=150, on_delete=models.CASCADE)
    number_of_seats = models.IntegerField()
    total_amount = models.IntegerField()
