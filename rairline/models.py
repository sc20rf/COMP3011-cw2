from django.db import models

#Create your models here.

class Airport(models.Model):
    airport_name = models.CharField(max_length=100)
    airport_code = models.CharField(max_length=3, primary_key=True)

    def __str__(self):
        return f'{self.airport_name}: {self.airport_code}'

class Flight(models.Model):
    flight_id = models.CharField(max_length=6, primary_key=True)
    capacity = models.PositiveSmallIntegerField()
    source = models.ForeignKey(Airport, to_field='airport_code', on_delete=models.PROTECT,
                                related_name='departures')
    destination = models.ForeignKey(Airport, to_field='airport_code', on_delete=models.PROTECT,
                                     related_name='arrivals')
    duration = models.PositiveSmallIntegerField()
    time = models.PositiveSmallIntegerField()
    business = models.BooleanField()
    eco_price = models.FloatField()
    bus_price = models.FloatField(blank=True, null=True)
    
    def __str__(self):
      return f'{self.flight_id}: {self.source} - {self.destination}'

class PaymentProvider(models.Model):
    pp_id = models.CharField(max_length = 3, primary_key=True)
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=100)

    def __str__(self):
      return f'{self.name}: {self.pp_id}'

class Passenger(models.Model):
    passenger_id = models.CharField(max_length = 6, primary_key=True)
    legal_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null = True)
    last_name = models.CharField(max_length=100, blank=True, null = True)
    date_of_birth = models.DateField()
    passport_no = models.CharField(max_length=9, unique=True)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=12, blank=True, null = True)
    
    def __str__(self):
        return f'{self.legal_name} - Passport Number : {self.passport_no}'

class Booking(models.Model):
    booking_id = models.CharField(max_length = 8, primary_key=True)
    flight_id = models.ForeignKey(Flight, to_field='flight_id', on_delete=models.PROTECT)
    passenger_id = models.ForeignKey(Passenger, to_field='passenger_id', on_delete=models.PROTECT)
    date_of_departure = models.DateField()
    booking_class = models.CharField(max_length=3, choices = [('eco', 'Economy'),('bus', 'Business')])
    payment_provider = models.ForeignKey(PaymentProvider, to_field='pp_id', on_delete=models.PROTECT, null=True)
    invoice_id = models.IntegerField(null=True)
    payment_received = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking ID: {self.booking_id} - Passenger: {self.passenger_id.legal_name} - Flight ID: {self.flight_id.flight_id}'