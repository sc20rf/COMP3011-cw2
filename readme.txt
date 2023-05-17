Name of my pythonanywhere domain - sc20rf.pythonanywhere.com

URL - https://sc20rf.pythonanywhere.com

URL to login to the admin site - https://sc20rf.pythonanywhere.com/admin/

Username for admin - ammar
Password for admin - simplepassword

-----------------------x----------------------------x-----------------------------x----------------------------

All the API Endpoints implemeted are in accordance with the group report.
The GET requests are as follows:

1. /airports
   Example - Visit https://sc20rf.pythonanywhere.com/rairlines/airports/
   This fetches a list of the available airport names and codes from the database

2. /flights
   Example - Visit https://sc20rf.pythonanywhere.com/rairlines/flights/?source=DEL&destination=LHR&date=2023-08-11
   This will give a list of available flights from the source (Airport code DEL in this example) to the destination (Airport code LHR) for the given date.

The POST requests are as follows:

1. /make-booking
   Example - sc20rf.pythonanywhere.com/rairlines/make-booking
   The test file make_booking_test.py shows an example payload that was tested for my service to ensure that it works as expected.

2. /invoice/{booking-id}
   Example - sc20rf.pythonanywhere.com/rairlines/invoice/{booking-id}
   The test file create_invoice_test.py shows an example payload that was tested for my service to ensure that it works as expected.

3. /confirm/{invoice-id}
   Example - sc20rf.pythonanywhere.com/rairlines/confirm/{invoice-id}
   The test file confirm_invoice_test.py shows an example that was tested for my service to ensure that it works as expected.

-----------------------x----------------------------x-----------------------------x----------------------------
