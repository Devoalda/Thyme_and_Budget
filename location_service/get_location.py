import os
import requests
import environ
from pathlib import Path
from requests import Response


class GeoOnemap:
    def __init__(self, postal_code=''):
        self.postal_code = postal_code
        self.HEADER = None
        self.api_key = None
        self.BASE_DIR = None
        self.longitude = None
        self.latitude = None
        self.address = None
        self.read_env()
        if postal_code:
            response = self.get_location_from_postal(self.postal_code)
            if response.status_code == 200 and response.json()['found'] > 0:
                self.longitude = response.json()['results'][0]['LONGITUDE']
                self.latitude = response.json()['results'][0]['LATITUDE']
                self.address = response.json()['results'][0]['ADDRESS']

    def read_env(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        environ.Env.read_env(os.path.join(self.BASE_DIR, '.env'))
        self.api_key = environ.Env()('ONEMAP_API_KEY', default='')
        self.HEADER = {"Authorization": self.api_key}

    # def update_api_key(self):
    #     update_api_key.update_api_key()
    #     self.read_env()

    def get_location_from_postal(self, postal_code) -> Response:
        """
        extract the location from the response of search_address_from_postal
        :param postal_code: Singapore postal code
        :return: api call response
        """

        url = "https://www.onemap.gov.sg/api/common/elastic/search?searchVal={}&returnGeom=Y&getAddrDetails=Y"
        response = requests.request("GET", url.format(postal_code), headers=self.HEADER)
        if response.status_code == 200:
            return response
        else:
            raise Exception('Error in get_location_from_postal: ' + response.text)

        # while True:
        #     response = requests.request("GET", url.format(postal_code), headers=self.HEADER)
        #     if response.status_code == 200:
        #         return response
        #     else:
        #         self.update_api_key()

    # def get_route(self, start_location, end_location, travel_type='walk') -> Response:
    #     """
    #     get the route from start location to end location from onemap api
    #     :param start_location: obtain from get_location_from_postal, in string with format 'latitude,longitude'
    #     :param end_location: obtain from get_location_from_postal, in string with format 'latitude,longitude'
    #     :param travel_type: 'walk', 'drive' or 'cycle', default is 'walk'
    #     :return: response from api call
    #     """
    #     params = {
    #         'start': start_location,
    #         'end': end_location,
    #         'routeType': travel_type
    #     }
    #     url = "https://www.onemap.gov.sg/api/public/routingsvc/route?{}".format(urlencode(params))
    #     while True:
    #         response = requests.request("GET", url, headers=self.HEADER)
    #         if response.status_code == 200:
    #             return response
    #         else:
    #             self.update_api_key()
