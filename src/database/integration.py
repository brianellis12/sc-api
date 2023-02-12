import os
import requests

url = os.environ.get('CENSUS_URL')
api_key = os.environ.get('CENSUS_KEY')
headers = {'api-key': api_key}
params = {'in': 'state:',
            'for': 'tract:',
            'get': ''}

class GeographicTypes:
    async def convert_coordinates(latitude: str, longitude: str):
        geo_params = {
            'y' : longitude,
            'x': latitude,
            'benchmark': '2020',
            'vintage': '2020',
            'format': 'json'
        }
        geo_url = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates?'
        response = requests.get(geo_url, params=geo_params)
        result = response.json()

        if(result['result']['geographies'] == {}):
            return "Invalid Coordinates"

        return result['result']['geographies']['Census Tracts'][0]['GEOID']
 
class CensusTypes: 
    #General/Population
    async def get_general_data(latitude: int, longitude: int):
        params += '01%20county:001' 
        params['for'] += '020500' 
        params['get'] += 'NAME,S0101_C01_001E'

    #Income
    async def get_income_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Age
    async def get_age_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'S0101_C01_030E,S0101_C01_028E,S0101_C01_023E,S0101_C01_025E,S0101_C01_019E' #Median Age, 65 and over, 15 - 45, 18 and over, 85 and over

        response = requests.get(url, headers=headers, params=params)
        
        return response.content
    #Sex
    async def get_sex_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Race
    async def get_race_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Citizenship/Place of Birth
    async def get_citizenship_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Education
    async def get_education_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Geographic mobility
    async def get_mobility_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Transportation
    async def get_transportation_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Employment
    async def get_employment_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Household
    async def get_household_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

    #Religions
    async def get_religion_data(latitude: int, longitude: int):
        params['in'] += '01%20county:001'
        params['for'] += '020500'
        params['get'] += 'NAME,S0101_C01_002E,S0101_C01_013E'

