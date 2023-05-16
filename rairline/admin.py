from django.contrib import admin
from .models import Airport, Flight, Booking, Passenger, PaymentProvider

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(PaymentProvider)
admin.site.register(Passenger)
admin.site.register(Booking)