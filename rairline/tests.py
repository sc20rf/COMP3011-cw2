# # from django.test import TestCase

# # Create your tests here.

# import requests

# url = 'http://127.0.0.1:8000/rairlines/make-booking/'

# # Sample payload data
# payload = {
#     'legal_name': 'Ruhma Fatima',
#     'first_name': 'Ruhma',
#     'last_name': 'Fatima',
#     'date_of_birth': '2001-11-09',
#     'passport_no': 'MZRK29065',
#     'email': 'ruhmafatima@gmail.com',
#     'contact_no': '9838097297',
#     'flight_code': 'R009HI',
#     'date_of_departure': '2023-07-04',
#     'class': 'eco'
# }

# # Send POST request with payload
# response = requests.post(url, data=payload)

# # Print response status code and content
# print(f'Response status code: {response.status_code}')
# print(f'Response content: {response.content.decode()}')

# # -------------------------------------------------

# import requests

# url = 'http://127.0.0.1:8000/rairlines/invoice/0ZD0TRV5/'

# # Sample payload data
# payload = {
#     'preferred_vendor': 'JB1'
# }

# # Send POST request with payload
# response = requests.post(url, data=payload)

# # Print response status code and content
# print(f'Response status code: {response.status_code}')
# print(f'Response content: {response.content.decode()}')

# # -------------------------------------------------

import requests
import json

url = 'http://127.0.0.1:8000/rairlines/confirm/0ZD0TRV5/'

response = requests.post(url)

print(f'Response status code: {response.status_code}')
print(f'Response content: {response.content.decode()}')

# import requests

# url = 'http://127.0.0.1:8000/rairlines/make-booking/'

# # Sample payload data
# payload = {
#     'legal_name': 'Joe Martin',
#     'first_name': 'Joe',
#     'last_name': 'Martine',
#     'date_of_birth': '1997-07-23',
#     'passport_no': 'ZHKH87650',
#     'email': 'martinjoe@gmail.com',
#     'contact_no': '7007860962',
#     'flight_code': 'R006FF',
#     'date_of_departure': '2023-12-06',
#     'class': 'eco'
# }

# # Send POST request with payload
# response = requests.post(url, data=payload)

# # Print response status code and content
# print(f'Response status code: {response.status_code}')
# print(f'Response content: {response.content.decode()}')
