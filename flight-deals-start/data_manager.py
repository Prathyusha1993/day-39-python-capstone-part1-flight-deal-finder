import requests
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth


load_dotenv()

retrieve_sheet_endpoint = 'https://api.sheety.co/6edff30815512dacea74b0a65cc2b64c/flightDealsForTravel/prices'

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.user = os.environ['SHEETY_USERNAME']
        self.password = os.environ['SHEETY_PASSWORD']
        self.authorization = HTTPBasicAuth(self.user, self.password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=retrieve_sheet_endpoint, auth=self.authorization)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data={
                'price':{
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(url=f'{retrieve_sheet_endpoint}/{city['id']}', json=new_data,auth=self.authorization)
            print(response.text)
