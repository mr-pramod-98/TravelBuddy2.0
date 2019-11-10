from django.contrib import admin
from .models import Packages, PackagesBookings, PackagesGuide, PackagesHotel, \
      VehicleAndGeneralDetails, DestinationDetails, HotelImages

# Register your models here.
admin.site.register(Packages)
admin.site.register(VehicleAndGeneralDetails)
admin.site.register(PackagesHotel)
admin.site.register(PackagesGuide)
admin.site.register(PackagesBookings)
admin.site.register(DestinationDetails)
admin.site.register(HotelImages)
