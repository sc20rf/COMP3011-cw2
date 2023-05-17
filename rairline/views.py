from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Airport, Flight, Booking, Passenger, PaymentProvider
from datetime import datetime
import json, random, string, requests

# Create your views here.

# The get_airport_info function is used for the /airports endpoint
# It returns a list of all the airports in the database
@csrf_exempt
def get_airport_info(request):

    if request.method == 'POST':
        return HttpResponseBadRequest('A POST request was received. This URL is set up for GET requests only')

    # List used to store airport name and code
    all_airports = []
    for airport in Airport.objects.all():
        all_airports.append({'airport_name': airport.airport_name, 'airport_code': airport.airport_code})

    return HttpResponse(json.dumps({
        'status_code': '200', 
        'airport_list': all_airports
    }))

# The get_flight_info function is used for the /flights endpoint
# It returns the flights avaliable from one airport to the other, for a particular date
@csrf_exempt
def get_flight_info(request):

    if request.method == 'POST':
        return HttpResponseBadRequest('A POST request was received. This URL is set up for GET requests only')

    # A list of required parameters for the GET request
    required_parameters = ['source', 'destination', 'date']
    for param in required_parameters:
        if not request.GET.get(param):
            return HttpResponseBadRequest(f"Missing required parameter: '{param}'")
   
    # Retrieve the source, destination and date from the request parameters
    source_code = request.GET.get('source')
    destination_code  = request.GET.get('destination')
    departure_date  = request.GET.get('date')
    
    # Check for validity of source and destination
    airports = [airport.airport_code for airport in Airport.objects.all()]
    if source_code not in airports:
        return HttpResponseBadRequest('Invalid Source')
    if destination_code not in airports:
        return HttpResponseBadRequest('Invalid Destination')

    # List used to store available flights 
    all_flights = []
    for flight in Flight.objects.filter(source = source_code, destination = destination_code):
        # Query for the Booking model to match bookings with the given the departure date and flight id
        prev_bookings = Booking.objects.filter(date_of_departure = departure_date, flight_id = flight.flight_id)
        current_capacity = flight.capacity - prev_bookings.count()

        # Dictionary to store the flight information
        flight_dict = {
            'flight_code': flight.flight_id,
            'duration': flight.duration,
            'flight_time': flight.time,
            'remaining_seats': current_capacity,
            'business_status': flight.business,
            'eco_price': flight.eco_price,
         'bus_price': flight.bus_price
        }

        all_flights.append(flight_dict)

        return HttpResponse(json.dumps({
            'status_code': '200',
            'flight_list': all_flights
        }))

# The make_booking function is used for the /make-booking endpoint
# It makes a passenger booking and returns the generated Booking ID and the details of payment providers
@csrf_exempt
def make_booking(request):
    
    if request.method == 'GET':
        return HttpResponseBadRequest('A GET request was received. This URL is set up for GET requests only')

    # A list of required parameters for the POST request
    param_names = ['legal_name', 'first_name', 'last_name', 'date_of_birth', 
                   'passport_no', 'email', 'contact_no', 'flight_code', 
                   'date_of_departure', 'class']
    param_values = {param: request.POST.get(param) for param in param_names}
    
    for param, value in param_values.items():
        if not value:
            return HttpResponseBadRequest(f'Missing required parameter: \'{param}\'')

    dob = datetime.strptime(param_values['date_of_birth'], '%Y-%m-%d').date()
    dep_date = datetime.strptime(param_values['date_of_departure'], '%Y-%m-%d').date()

    # Required validation checks
    if dob.year < 1900 or dob.year > 2023:
        return HttpResponseBadRequest('Invalid Date of Birth. Please enter a value between 1900 and 2023 for the year of birth.')
    if dep_date.year < 2023 or dep_date.year > 2025:
        return HttpResponseBadRequest('Invalid Date of Departure. Bookings only between the year 2023 and 2025 are allowed.')
    if len(param_values['passport_no']) != 9:
        return HttpResponseBadRequest('Inavlid Passport Number. Ensure that there are 9 characters in your passport number.')
    if '@' not in param_values['email']:
        return HttpResponseBadRequest("Invalid Email address.")
    if not Flight.objects.filter(flight_id=param_values['flight_code']).exists():
        return HttpResponseBadRequest("Invalid flight code")
    if param_values['class'] not in ['eco', 'bus']:
        return HttpResponseBadRequest("Invalid Booking Class - \'eco/bus\'")

    # Creates a new passenger or fetch the existing one based on the passport number
    passenger, created = Passenger.objects.get_or_create(
        passport_no=param_values['passport_no'],
        defaults={
            'passenger_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
            'legal_name': param_values['legal_name'],
            'first_name': param_values.get('first_name', ''),
            'last_name': param_values.get('last_name', ''),
            'date_of_birth': param_values['date_of_birth'],
            'email': param_values['email'],
            'contact_no': param_values.get('contact_no', '')
        }
    )

    # Check if the email address is the same for an already existing passenger booking
    if not created and param_values['email'] != passenger.email:
        return HttpResponseBadRequest('This Email ID is already registered for a passenger. Please use a different email address')

    # Check if a booking with the same flight code, passenger id, and departure date already exists
    check_booking = Booking.objects.filter(
        flight_id=param_values['flight_code'],
        passenger_id=passenger.passenger_id,
        date_of_departure=param_values['date_of_departure']
    )

    if check_booking.exists():
        check_booking_id = check_booking[0].booking_id
        return HttpResponseBadRequest(f"This booking already exists. Refer booking id {check_booking_id}")

    new_booking = Booking.objects.create(
        booking_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        flight_id=Flight.objects.get(flight_id=param_values['flight_code']),
        passenger_id=passenger,
        date_of_departure=param_values['date_of_departure'],
        booking_class=param_values['class'],
        invoice_id=None,
        payment_received=False
    )
    
    # List of payment providers in the group
    providers = [{'pp_code': pp.pp_id, 'pp_name': pp.name} for pp in PaymentProvider.objects.all()]

    return HttpResponse(json.dumps({
        'status_code': '200', 
        'booking_id': new_booking.booking_id,
        'pp_list': providers
    }))

# The create_invoice function is used for the /invoice/{booking-id} endpoint
# It generates an invoice by calling the API endpoint of the preferred payment provider
@csrf_exempt
def create_invoice(request, booking_id):

    if request.method == 'GET':
        return HttpResponseBadRequest('A GET request was received. This URL is set up for POST requests only')

    # Extracts the preferred vendor from the request
    preferred_vendor_param = request.POST.get('preferred_vendor')

    # Checks if the preferred vendor parameter is missing from the request
    if not preferred_vendor_param:
        return HttpResponseBadRequest('Missing required parameter: \'preferred_vendor\'')
    # Performs validation for the preferred vendor
    if not PaymentProvider.objects.filter(pp_id=preferred_vendor_param).exists():
        return HttpResponseBadRequest('\'preferred_vendor\' is invalid')
    
    # Retrieves the passenger booking for given booking id
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponseBadRequest('\'booking_id\' is invalid')

    # Check if the booking already has an invoice
    if booking.invoice_id is not None:
        return HttpResponseBadRequest(f'Given \'booking_id\': {booking_id} already has an invoice: {booking.invoice_id}')

    booking.payment_provider = PaymentProvider.objects.get(pp_id=preferred_vendor_param)

    given_provider = PaymentProvider.objects.get(pp_id=preferred_vendor_param)
    url_to_call = given_provider.url + 'invoice/'

    # Gets the flight associated with the booking and determine the amount to be invoiced
    flight = Flight.objects.get(flight_id=booking.flight_id.flight_id)
    amount = flight.eco_price if booking.booking_class == 'eco' else flight.bus_price
    amount = int(amount * 100)

    # Defines the payload for the POST request to the payment provider's API
    input_data = {
        "api_key": '9090',
        "amount": amount,
        "metadata": []
    }

    response = requests.post(url_to_call, data=json.dumps(input_data), headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        return HttpResponse(f'Error: {response.reason}')

    response_data = response.json()
    invoice_id = response_data['invoice_id']
    booking.invoice_id = invoice_id
    booking.save()

    return HttpResponse(json.dumps({
        'status_code': '200', 
        'invoice_id': invoice_id
    }))

# The confirm_invoice function is used for the /confirm/{booking-id} endpoint
# It confirms the status of the booking invoice by calling the API endpoint of the payement provider
# It also updates the Booking database accordingly
@csrf_exempt
def confirm_invoice(request, booking_id):

    if request.method == 'GET':
        return HttpResponseBadRequest('A GET request was received. This URL is set up for POST requests only')

    # Retrieves the passenger booking for given booking id
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponseBadRequest('\'booking_id\' is invalid')

    # Gets the payment provider details for the booking
    provider = PaymentProvider.objects.get(pp_id=booking.payment_provider.pp_id)
    # The URL to call the payment provider's API to confirm the invoice
    url_to_call = provider.url + f'invoice/{booking.invoice_id}/'
    # Define the payload for the GET request to the payment provider's API
    input_json = json.dumps({'api_key': '9090'})

    response = requests.get(url_to_call, data=input_json, headers={'Content-Type': 'application/json'})
    
    if response.status_code != 200:
        return HttpResponse(f"Error: {response.reason}")
    
    response_data = response.json()
    payment_status = response_data['paid']

    booking.payment_received = payment_status
    booking.save()

    return HttpResponse(json.dumps({
        'status_code': '200',
        'payment_status': payment_status
    }))

