import os
import requests

async def get_location_data(latitude: int, longitude: int):
    url = os.environ.get('CENSUS_URL')
    api_key = os.environ.get('CENSUS_KEY')
    headers = {'api-key': api_key}
    response = requests.get(url, headers=headers)
    print(response.content)
    return response.content


