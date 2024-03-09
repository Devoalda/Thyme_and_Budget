import requests
from requests import Response


def get_location_from_postal(postal_code) -> Response:
    """
    extract the location from the response of search_address_from_postal
    :param postal_code: Singapore postal code
    :return: api call response
    """

    url = "https://www.onemap.gov.sg/api/common/elastic/search?searchVal={}&returnGeom=Y&getAddrDetails=Y"
    response = requests.request("GET", url.format(postal_code))
    if response.status_code == 200:
        return response
    else:
        raise Exception('Error in get_location_from_postal: ' + response.text)


class GeoOnemap:
    def __init__(self, postal_code=''):
        self.postal_code = postal_code
        self.longitude = None
        self.latitude = None
        self.address = None
        if postal_code:
            response = get_location_from_postal(self.postal_code)
            if response.status_code == 200 and response.json()['found'] > 0:
                self.longitude = response.json()['results'][0]['LONGITUDE']
                self.latitude = response.json()['results'][0]['LATITUDE']
                self.address = response.json()['results'][0]['ADDRESS']
            else:
                raise Exception('Error in GeoOnemap: ' + response.text)
