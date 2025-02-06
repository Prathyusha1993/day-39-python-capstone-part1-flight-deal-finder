from dotenv import load_dotenv
import os

load_dotenv()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_key = os.environ['AMADEUS_API_KEY']
        self.api_secret = os.environ['AMADEUS_API_SECRET']
        self.token = self.get_new_token()

    def get_destination_code(self, city_name):
        code = 'TESTING'
        return code

    def get_new_token(self):
        pass