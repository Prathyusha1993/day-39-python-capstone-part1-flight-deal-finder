#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import smtplib
import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flights
from dotenv import load_dotenv
import os


load_dotenv()
MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
ORIGINAL_CITY_IATA = 'LON'

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
print(sheet_data)
flight_search = FlightSearch()


# UPDATE AIRPORT CODEIN GOOGLE SHEET
for row in sheet_data:
    if row['iataCode'] == '':
        row['iataCode'] = flight_search.get_destination_code(row['city'])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f'sheet_data:\n {sheet_data}')

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# SEARCH FOR FLIGHTS
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days= (6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}....")
    flights = flight_search.check_flights(
        ORIGINAL_CITY_IATA,
        destination['iataCode'],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flights(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    time.sleep(2)

    # print(type(cheapest_flight.price))
    # print(type(destination['lowestPrice']))
    try:
        price = int(cheapest_flight.price[0])
    except (TypeError, ValueError, IndexError):
        price = float('inf')

    if price < destination['lowestPrice']:
        print(f"Lower price flight found to {destination['city']}!")

        # i used smtplib you can also use twilio as sms
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=f'Subject:Info about cheapest flight: £{cheapest_flight.price} from '
                                    f'{cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}'
                                    f'on {cheapest_flight.out_date} until {cheapest_flight.return_date}.')
            connection.close()
