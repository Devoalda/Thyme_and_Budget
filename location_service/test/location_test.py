import unittest
from location_service.get_location import GeoOnemap


class TestLocationService(unittest.TestCase):
    def setUp(self):
        self.postal_code = '670656'
        self.postal_code_2 = '569830'
        self.geo_onemap = GeoOnemap(self.postal_code)

    def test_search_address_from_postal(self):
        response = self.geo_onemap.get_location_from_postal(self.postal_code)
        print("address: ", self.geo_onemap.address)
        print("latitude: ", self.geo_onemap.latitude)
        print("longitude: ", self.geo_onemap.longitude)
        self.assertEqual(response.status_code, 200)

    # def test_get_route(self):
    #     start_location_response = self.geo_onemap.get_location_from_postal(self.postal_code)
    #     end_location_response = self.geo_onemap.get_location_from_postal(self.postal_code_2)
    #
    #     start_location = str(start_location_response.json()['results'][0]['LATITUDE']) + ',' + str(
    #         start_location_response.json()['results'][0]['LONGITUDE'])
    #     end_location = str(end_location_response.json()['results'][0]['LATITUDE']) + ',' + str(
    #         end_location_response.json()['results'][0]['LONGITUDE'])
    #
    #     response = self.geo_onemap.get_route(start_location, end_location)
    #     print(response.json())
    #     self.assertEqual(response.status_code, 200)
