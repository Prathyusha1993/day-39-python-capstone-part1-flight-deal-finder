
from datetime import datetime
from traceback import print_tb

from dotenv import load_dotenv
import os
import requests

load_dotenv()
token_endpoint = 'https://test.api.amadeus.com/v1/security/oauth2/token'
iata_endpoint = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
flight_endpoint = 'https://test.api.amadeus.com/v2/shopping/flight-offers'


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_key = os.environ['AMADEUS_API_KEY']
        self.api_secret = os.environ['AMADEUS_API_SECRET']
        self.token = self.get_new_token()

    def get_destination_code(self, city_name):
        # print(f'Using this token to get destination {self.token}')
        headers = {'Authorization': f"Bearer {self.token}"}
        query = {
            'keyword': city_name,
            'max': '2',
            'include': 'AIRPORTS',
        }
        response = requests.get(url=iata_endpoint, headers=headers, params=query)

        print(f"Status Code {response.status_code}. Airport IATA:  {response.text}")
        try:
            code = response.json()['data'][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return 'N/A'
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return 'Not Found'

        return code


    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        response = requests.post(url=token_endpoint,headers=header,data=body)
        print(f'Your token is {response.json()['access_token']}')
        print(f'Your token expires in {response.json()['expires_in']} seconds.')
        return response.json()['access_token']

    def check_flights(self, original_city_code, destination_city_code, from_time, to_time):
        # print(f'Using this token to get destination {self.token}')
        headers = {'Authorization': f"Bearer {self.token}"}
        parameters = {
            'originLocationCode': original_city_code,
            'destinationLocationCode': destination_city_code,
            'departureDate': from_time.strftime('%Y-%m-%d'),
            'returnDate': to_time.strftime('%Y-%m-%d'),
            'adults': 1,
            'nonStop': 'true',
            'currencyCode': 'GBP',
            'max': '10'
        }
        response = requests.get(url=flight_endpoint, headers=headers, params=parameters)
        # print(response.json()['data'][0])
        if response.status_code != 200:
            print(f'check_flight() response code: {response.status_code}')
            print('There was a problem with the flight search \n. for details check api documentation.')
            print('Response Body:', response.text)
            return None

        return response.json()
