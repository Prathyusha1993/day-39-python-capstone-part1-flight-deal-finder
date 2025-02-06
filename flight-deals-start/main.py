#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flights

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
