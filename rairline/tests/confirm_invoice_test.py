import requests

# Test for URL: /confirm/{booking-id}

# The booking id in the URL can be changed to test for another booking

url = 'http://127.0.0.1:8000/rairlines/confirm/ZXFZDJAE/'

# Send POST request
response = requests.post(url)

print(f'Response status code: {response.status_code}')
print(f'Response content: {response.content.decode()}')

# In the directory 'tests' run the command: python confirm_invoice_test.py > confirm_invoice_test.html