import requests

# Test for URL: /invoice/{booking-id}

# The booking id in the URL can be changed to test for another booking
url = 'http://127.0.0.1:8000/rairlines/invoice/ZXFZDJAE/'

# Sample payload data for the POST request
# The preferred vendor can be chosen from - NN7, M2A, JB1, CO9
payload = {
    'preferred_vendor': 'M2A'
}

# Send POST request
response = requests.post(url, data=payload)
print(f'Response status code: {response.status_code}')
print(f'Response content: {response.content.decode()}')

# In the directory 'tests' run the command: python create_invoice_test.py > create_invoice_test.html