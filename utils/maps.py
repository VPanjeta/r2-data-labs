import requests
import os
import urllib.parse

"""
This class manager all maps related images and data from google maps
"""
class MapsManager:

    def __init__(self):
        self.key = os.getenv("GOOGLE_MAPS_API_KEY")

    def get_lat_long(self, location):
        url_params = urllib.parse.urlencode({
            'key': self.key,
            'address': location
        })
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?{url_params}')

        resp_json_payload = response.json()
        return resp_json_payload['results'][0]['geometry']['location']

    def get_location_image(self, location, zoom=10, type='terrain'):
        lat_long = self.get_lat_long(location)
        url_params = urllib.parse.urlencode({
            'key': self.key,
            'center': f"{lat_long['lat']},{lat_long['lng']}",
            'zoom': zoom,
            'size': '640x300',
            'scale': 2,
            'maptype': type,
        })
        res = requests.get(f'https://maps.googleapis.com/maps/api/staticmap?{url_params}')
        return res.content


if __name__ == "__main__":
    MapsManager().get_location_image("Bangalore")
