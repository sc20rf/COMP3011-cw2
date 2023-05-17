import requests

# Test for URL: /make-booking

url = 'http://127.0.0.1:8000/rairlines/make-booking/'

# Sample payload data for the make_booking POST request
# Can be changed to test for another passenger
payload = {
    'legal_name': 'William Herondale',
    'first_name': 'William',
    'last_name': 'Herondale',
    'date_of_birth': '1997-11-09',
    'passport_no': 'WARK25679',
    'email': 'herondale@gmail.com',
    'contact_no': '7786653417',
    'flight_code': 'R003CC',
    'date_of_departure': '2023-07-04',
    'class': 'eco'
}

# Send POST request
response = requests.post(url, data=payload)
print(f'Response status code: {response.status_code}')
print(f'Response content: {response.content.decode()}')

# In the directory 'tests' run the command: python make_booking_test.py > make_booking_test.html